# Test App (Android)

A small test web app — counter, to-do list and a device check — that you can put on an Android phone in two ways.

## 1. Download the APK (real Android app)

Every push that changes `android-test-app/` runs the **Build Android test app** GitHub Action. It wraps `www/` in a native app with [Capacitor](https://capacitorjs.com/), builds a debug APK and publishes it to the **`android-test-app-latest`** release.

1. On your phone, open the repository's **Releases** page and pick **Android test app (latest build)**.
2. Tap **test-app.apk** to download it.
3. Open the file and allow your browser to install unknown apps when Android asks.

Each build is signed with a fresh debug key, so to install a newer build, uninstall the old one first.

## 2. Install as a web app (PWA)

Host `www/` on any HTTPS site (GitHub Pages, Netlify, …), open it in Chrome on Android and tap **Add to home screen** in the app or **Install app** in Chrome's menu. It works offline after the first visit.

## Run locally

```bash
cd android-test-app
npm run serve        # http://localhost:8080
```

To build the APK yourself you need Node 22, JDK 21 and the Android SDK:

```bash
npm ci
npx cap add android && ./scripts/apply-icon.sh && npx cap sync android
cd android && ./gradlew assembleDebug   # app/build/outputs/apk/debug/app-debug.apk
```
