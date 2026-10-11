plugins { id("com.android.application"); id("org.jetbrains.kotlin.android"); id("com.chaquo.python") }
val ksPath = System.getenv("AMELIA_KEYSTORE_PATH")
val ksPass = System.getenv("AMELIA_KEYSTORE_PASSWORD")
val ksAlias = System.getenv("AMELIA_KEY_ALIAS")
val hasStableSigning = listOf(ksPath, ksPass, ksAlias).all { !it.isNullOrBlank() }
android {
    namespace = "com.amelia.driftg1"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.amelia.driftg1"
        minSdk = 24
        targetSdk = 34
        versionCode = (System.getenv("GITHUB_RUN_NUMBER") ?: "1").toInt()
        versionName = "1.0-G1"
        ndk { abiFilters += listOf("armeabi-v7a", "arm64-v8a", "x86_64") }
    }
    signingConfigs {
        if (hasStableSigning) {
            create("amelia") {
                storeFile = file(ksPath!!); storePassword = ksPass
                keyAlias = ksAlias; keyPassword = ksPass
            }
        }
    }
    buildTypes { getByName("debug") { if (hasStableSigning) signingConfig = signingConfigs.getByName("amelia") } }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
}
kotlin { jvmToolchain(17) }
chaquopy { defaultConfig { version = "3.11"; pyc { src = false } } }
