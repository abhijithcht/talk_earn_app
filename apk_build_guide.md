# 📱 Talk & Earn: APK Build Guide

Follow these steps to generate your Android APK and install it on your phone.

## Prerequisites
1.  **Download & Install Android Studio**: [https://developer.android.com/studio](https://developer.android.com/studio)
2.  **Connect your Phone**: Enable "USB Debugging" in your phone's Developer Options and connect it to your computer.

---

## Step 1: Open the Project
1.  Launch **Android Studio**.
2.  Select **"Open"** or **"Import Project"**.
3.  Navigate to your project folder (e.g. `C:\Projects\talk_earn_app\talk_earn_app`).
4.  Inside that folder, select the **`android`** folder and click **OK**.
5.  Wait for Android Studio to finish "Syncing" (look at the bottom progress bar).

## Step 2: Configure Network Permissions
I have already set up the basic config, but Android Studio might ask to "Update Gradle". You can click **"Update"** if it prompts you.

## Step 3: Build the APK
1.  In the top menu, go to **Build** > **Build Bundle(s) / APK(s)** > **Build APK(s)**.
2.  Android Studio will start building. This takes 1–3 minutes.
3.  Once finished, a small notification will appear in the bottom right. Click **"locate"** to find your `app-debug.apk`.

## Step 4: Install on your Phone
1.  Copy the `app-debug.apk` file to your phone (via USB or Google Drive).
2.  Open the file on your phone and click **Install**.
    *   *Note: You may need to "Allow installation from unknown sources".*

---

## 💡 Pro Tip: Live Testing
If you want to see changes instantly while your phone is plugged in:
1.  Click the **Green Play Button** (triangle) at the top of Android Studio.
2.  Select your connected phone.
3.  The app will open automatically on your device!

## ⚠️ Connectivity Note
Ensure your phone is on the **same Wi-Fi** as your computer so it can talk to the backend server at `192.168.18.225`.
