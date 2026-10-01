plugins { id("com.android.application"); id("org.jetbrains.kotlin.android"); id("com.chaquo.python") }

// Repository secrets may provide a stable signing key so successive builds install over
// one another and filesDir survives updates. No private signing key is committed.
// Without the secrets, Android's normal debug signing is used as a CI fallback.
val ksPath: String? = System.getenv("AMELIA_KEYSTORE_PATH")
val ksPass: String? = System.getenv("AMELIA_KEYSTORE_PASSWORD")
val ksAlias: String? = System.getenv("AMELIA_KEY_ALIAS")
val ksKeyPass: String? = System.getenv("AMELIA_KEY_PASSWORD")
val hasStableSigning = listOf(ksPath, ksPass, ksAlias, ksKeyPass).all { !it.isNullOrBlank() }

android {
    namespace = "com.amelia.one"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.amelia.one"
        minSdk = 24
        targetSdk = 34
        versionCode = (System.getenv("GITHUB_RUN_NUMBER") ?: "1").toInt()
        versionName = "1.0-M1.1"
        ndk { abiFilters += listOf("armeabi-v7a", "arm64-v8a") }
    }
    signingConfigs {
        if (hasStableSigning) {
            create("amelia") {
                storeFile = file(ksPath!!)
                storePassword = ksPass
                keyAlias = ksAlias
                keyPassword = ksKeyPass
            }
        }
    }
    buildTypes {
        getByName("debug") {
            if (hasStableSigning) signingConfig = signingConfigs.getByName("amelia")
        }
    }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
}
kotlin { jvmToolchain(17) }

// M1.1 keeps canonical .py source inside the APK. Startup hashes the exact source bytes
// returned by the import loader; compiled-only .pyc packaging would make that impossible.
chaquopy { defaultConfig { version = "3.11"; pyc { src = false } } }
