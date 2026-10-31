#!/usr/bin/env node
// P3.26 prospectively fixed, dual-relay verified drand acquisition.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { HttpCachingChain, HttpChainClient } from 'drand-client';
const CHAIN_HASH='8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce';
const PUBLIC_KEY='868f005eb8e6e4ca0a47c8a77ceaa5309a47978a7c71bc5cce96366b5d7a569937c529eeda66c7293784a9402801af31';
const GENESIS=1595431050, PERIOD=30, COUNT=24;
const REG_SHA=fs.readFileSync('experiments/p326/SEALED_REGISTRATION_SHA.txt','utf8').trim();
const SEAL_UNIX=Number(process.env.SEAL_UNIX||0);
if(!Number.isInteger(SEAL_UNIX)||SEAL_UNIX<=0) throw new Error('SEAL_UNIX missing');
const NOT_BEFORE=SEAL_UNIX+90;
const START_ROUND=Math.ceil((NOT_BEFORE-GENESIS)/PERIOD)+1;
const START_TIME=GENESIS+(START_ROUND-1)*PERIOD;
if(START_TIME<NOT_BEFORE) throw new Error('scheduled start precedes registration hold');
const options={disableBeaconVerification:false,noCache:true,chainVerificationParams:{chainHash:CHAIN_HASH,publicKey:PUBLIC_KEY}};
const clients=['https://api.drand.sh','https://drand.cloudflare.com'].map(url=>new HttpChainClient(new HttpCachingChain(url,options),options));
const OUT='experiments/p326/results';
fs.mkdirSync(OUT,{recursive:true});
const logPath=OUT+'/ACQUISITION.jsonl';
if(fs.existsSync(logPath)||fs.existsSync(OUT+'/BEACON.json')) throw new Error('create-only acquisition output already exists');
let previous='0'.repeat(64);
const log=fs.openSync(logPath,'wx');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const canonical=o=>JSON.stringify(o,Object.keys(o).sort());
const normalize=b=>({round:Number(b.round),signature:String(b.signature).toLowerCase(),previous_signature:String(b.previous_signature??'').toLowerCase(),randomness:String(b.randomness).toLowerCase()});
function field(randomness,index){
 const src=Buffer.from(randomness,'hex');
 const seed=crypto.createHash('sha256').update(Buffer.from('P3.26-FIELD-v1\0','utf8')).update(src).update(Buffer.from(BigInt(index).toString(16).padStart(16,'0'),'hex')).digest();
 const vals=[];let counter=0;
 while(vals.length<10){
  const block=crypto.createHash('sha256').update(seed).update(Buffer.from(counter.toString(16).padStart(8,'0'),'hex')).digest();counter++;
  for(let i=0;i<32&&vals.length<10;i+=8){
   const word=block.readBigUInt64BE(i);
   vals.push(Number(word)/18446744073709551616*2-1);
  }
 }
 const mean=vals.reduce((a,b)=>a+b,0)/10, centered=vals.map(x=>x-mean);
 const norm=Math.sqrt(centered.reduce((a,b)=>a+b*b,0));
 if(norm<=1e-12) throw new Error('zero mapped field');
 return centered.map(x=>x/norm);
}
const get=async(c,n)=>{let err;for(let i=0;i<180;i++){try{return await c.get(n)}catch(e){err=e;await new Promise(r=>setTimeout(r,5000))}}throw new Error('round '+n+' unavailable: '+err)};
const records=[];
for(let i=0;i<COUNT;i++){
 const round=START_ROUND+i;
 const [x0,y0]=await Promise.all([get(clients[0],round),get(clients[1],round)]);
 const x=normalize(x0),y=normalize(y0);
 if(JSON.stringify(x)!==JSON.stringify(y)) throw new Error('relay mismatch at round '+round);
 if(x.round!==round) throw new Error('unexpected round '+x.round);
 const local=sha(Buffer.from(x.signature,'hex'));
 if(local!==x.randomness) throw new Error('randomness digest mismatch at '+round);
 const row={packet_index:i,round,scheduled_unix:GENESIS+(round-1)*PERIOD,signature:x.signature,previous_signature:x.previous_signature,randomness:x.randomness,local_randomness_sha256:local,field:field(x.randomness,i)};
 const payload=canonical(row),digest=sha(Buffer.from(previous+payload,'utf8'));
 const line=JSON.stringify({payload_json:payload,previous_digest:previous,record_digest:digest})+'\n';
 fs.writeSync(log,line);fs.fsyncSync(log);previous=digest;records.push(row);
 console.log(JSON.stringify({packet_index:i,round,record_digest:digest}));
}
fs.closeSync(log);
const beacon={schema:'amelia-p326-drand-field-v1',sealed_registration_sha:REG_SHA,seal_unix:SEAL_UNIX,not_before_unix:NOT_BEFORE,start_round:START_ROUND,start_round_scheduled_unix:START_TIME,chain:{name:'drand-default-mainnet',chain_hash:CHAIN_HASH,public_key:PUBLIC_KEY,genesis_unix:GENESIS,period_seconds:PERIOD,client:'drand-client@1.4.2',verification_enabled:true,relays:['https://api.drand.sh','https://drand.cloudflare.com']},rounds:records,acquisition_log_head_sha256:previous};
fs.writeFileSync(OUT+'/BEACON.json',JSON.stringify(beacon,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({start_round:START_ROUND,end_round:START_ROUND+COUNT-1,packets:COUNT,acquisition_log_head_sha256:previous}));
