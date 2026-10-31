#!/usr/bin/env node
// P3.24 prospective histogram-balanced drand acquisition.
// No Numogram code or Amelia state is imported here.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { HttpCachingChain, HttpChainClient } from 'drand-client';

const CHAIN_HASH='8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce';
const PUBLIC_KEY='868f005eb8e6e4ca0a47c8a77ceaa5309a47978a7c71bc5cce96366b5d7a569937c529eeda66c7293784a9402801af31';
const GENESIS=1595431050;
const PERIOD=30;
const COUNT=24;
const WINDOW=30;
const REG_SHA=fs.readFileSync('experiments/p324/SEALED_REGISTRATION_SHA.txt','utf8').trim();
const SEAL_UNIX=Number(process.env.SEAL_UNIX || 0);
if(!Number.isInteger(SEAL_UNIX) || SEAL_UNIX<=0) throw new Error('SEAL_UNIX missing');
const NOT_BEFORE=SEAL_UNIX+90;
const START_ROUND=Math.ceil((NOT_BEFORE-GENESIS)/PERIOD)+1;
const START_TIME=GENESIS+(START_ROUND-1)*PERIOD;
if(START_TIME<NOT_BEFORE) throw new Error('round calculation violated not-before');

const options={
  disableBeaconVerification:false,
  noCache:true,
  chainVerificationParams:{chainHash:CHAIN_HASH, publicKey:PUBLIC_KEY}
};
const clients=[
  new HttpChainClient(new HttpCachingChain('https://api.drand.sh',options),options),
  new HttpChainClient(new HttpCachingChain('https://drand.cloudflare.com',options),options),
];

function sleep(ms){return new Promise(r=>setTimeout(r,ms));}
function sha256Hex(buf){return crypto.createHash('sha256').update(buf).digest('hex');}
function normalize(b){
  return {
    round:Number(b.round),
    signature:String(b.signature).toLowerCase(),
    previous_signature:String(b.previous_signature ?? '').toLowerCase(),
    randomness:String(b.randomness).toLowerCase()
  };
}
async function getWithRetry(client,round){
  let last;
  for(let i=0;i<180;i++){
    try{return await client.get(round);}catch(e){last=e; await sleep(5000);}
  }
  throw new Error(`round ${round} unavailable after retries: ${last}`);
}

const BASE=[];
for(let z=0;z<10;z++) for(let k=0;k<3;k++) BASE.push(z);
if(BASE.length!==WINDOW) throw new Error('base multiset length');

function wordStream(label,randomness){
  let counter=0, pool=Buffer.alloc(0), offset=0;
  return ()=>{
    if(offset+4>pool.length){
      pool=crypto.createHash('sha256')
        .update(label,'utf8')
        .update(Buffer.from(randomness,'hex'))
        .update(':','utf8')
        .update(String(counter++),'utf8')
        .digest();
      offset=0;
    }
    const x=pool.readUInt32BE(offset); offset+=4; return x;
  };
}
function permute(label,randomness){
  const a=[...BASE], next=wordStream(label,randomness);
  for(let i=a.length-1;i>0;i--){
    const n=i+1;
    const limit=Math.floor(0x100000000/n)*n;
    let x; do{x=next();}while(x>=limit);
    const j=x%n;
    [a[i],a[j]]=[a[j],a[i]];
  }
  return a;
}
function invariant(a){
  if(a.length!==WINDOW) return false;
  const c=Array(10).fill(0);
  for(const z of a){if(!Number.isInteger(z)||z<0||z>9)return false;c[z]++;}
  return c.every(x=>x===3);
}

const out={
  schema:'amelia-p324-drand-balanced-order-v1',
  sealed_registration_sha:REG_SHA,
  seal_unix:SEAL_UNIX,
  not_before_unix:NOT_BEFORE,
  chain:{
    name:'drand-default-mainnet',
    chain_hash:CHAIN_HASH,
    public_key:PUBLIC_KEY,
    genesis_unix:GENESIS,
    period_seconds:PERIOD,
    client:'drand-client@1.4.2',
    verification_enabled:true,
    relays:['https://api.drand.sh','https://drand.cloudflare.com']
  },
  base_multiset:BASE,
  encoding_a_domain:'P3.24-A',
  encoding_b_domain:'P3.24-B',
  start_round:START_ROUND,
  start_round_scheduled_unix:START_TIME,
  rounds:[]
};

for(let k=0;k<COUNT;k++){
  const round=START_ROUND+k;
  const [a0,b0]=await Promise.all([getWithRetry(clients[0],round),getWithRetry(clients[1],round)]);
  const a=normalize(a0), b=normalize(b0);
  if(JSON.stringify(a)!==JSON.stringify(b)) throw new Error(`relay mismatch at round ${round}`);
  if(a.round!==round) throw new Error(`unexpected round ${a.round} != ${round}`);
  const local=sha256Hex(Buffer.from(a.signature,'hex'));
  if(local!==a.randomness) throw new Error(`randomness hash mismatch at round ${round}`);
  const A=permute('P3.24-A',a.randomness);
  const B=permute('P3.24-B',a.randomness);
  if(!invariant(A)||!invariant(B)) throw new Error(`balance invariant failed at round ${round}`);
  if([...A].sort((x,y)=>x-y).join(',')!==[...B].sort((x,y)=>x-y).join(',')) throw new Error('A/B multiset mismatch');
  out.rounds.push({
    round,
    scheduled_unix:GENESIS+(round-1)*PERIOD,
    signature:a.signature,
    previous_signature:a.previous_signature,
    randomness:a.randomness,
    local_randomness_sha256:local,
    encoding_a:A,
    encoding_b:B
  });
}

if(out.rounds.length!==COUNT) throw new Error('wrong beacon count');
fs.mkdirSync('experiments/p324/results',{recursive:true});
fs.writeFileSync('experiments/p324/results/BEACON.json',JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify({
  sealed_registration_sha:REG_SHA,
  seal_unix:SEAL_UNIX,
  not_before_unix:NOT_BEFORE,
  start_round:START_ROUND,
  start_round_scheduled_unix:START_TIME,
  end_round:START_ROUND+COUNT-1,
  windows:COUNT,
  balanced_signal_length:WINDOW
},null,2));
