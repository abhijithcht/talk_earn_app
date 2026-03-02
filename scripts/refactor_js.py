import re

file_path = "www/app.js"
with open(file_path, "r", encoding="utf-8") as f:
    js = f.read()

# Remove initial config block (API_BASE, WS_BASE)
js = re.sub(r"const LOCAL_IP = .*?;", "", js, flags=re.DOTALL)
js = re.sub(r"const isMobile = .*?;", "", js, flags=re.DOTALL)
js = re.sub(r"const API_BASE = .*?;", "", js, flags=re.DOTALL)
js = re.sub(r"const WS_BASE = .*?;", "", js, flags=re.DOTALL)

# Replace WS_BASE with window.apiService.WS_BASE
js = js.replace("WS_BASE", "window.apiService.WS_BASE")

# 1. Register
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/auth/register`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{ 'Content-Type': 'application/json' \},[\s\n]+body: JSON.stringify\(\{ email, password, gender \}\)[\s\n]+\}\);",
    r"const res = await window.apiService.register(email, password, gender);",
    js
)

# 2. Login (normal)
js = re.sub(
    r"const resObj = await fetch\(`\$\{API_BASE\}/auth/token`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{ 'Content-Type': 'application/x-www-form-urlencoded' \},[\s\n]+body: `username=\$\{encodeURIComponent\(email\)\}&password=\$\{encodeURIComponent\(password\)\}`[\s\n]+\}\);",
    r"const resObj = await window.apiService.login(email, password);",
    js
)

# 3. Verify Email
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/auth/verify-email`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{ 'Content-Type': 'application/json' \},[\s\n]+body: JSON.stringify\(\{ email: pendingEmail, otp_code \}\)[\s\n]+\}\);",
    r"const res = await window.apiService.verifyEmail(pendingEmail, otp_code);",
    js
)

# 4. Login (auto login after verify) - Has a bug in original code (sent JSON), let's fix it by calling apiService.login
js = re.sub(
    r"const resObj = await fetch\(`\$\{API_BASE\}/auth/token`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{ 'Content-Type': 'application/json' \},[\s\n]+body: JSON.stringify\(\{ email: pendingEmail, password: pendingPassword \}\)[\s\n]+\}\);",
    r"const resObj = await window.apiService.login(pendingEmail, pendingPassword);",
    js
)

# 5. Get Profile /me
js = re.sub(
    r"const meRes = await fetch\(`\$\{API_BASE\}/profile/me`, \{[\s\n]+headers: \{ 'Authorization': `Bearer \$\{currentToken\}` \}[\s\n]+\}\);",
    r"const meRes = await window.apiService.getProfile();",
    js
)

# 6. Get Wallet Balance
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/wallet/balance`, \{[\s\n]+headers: \{[\s\n]+'Content-Type': 'application/json',[\s\n]+'Authorization': `Bearer \$\{currentToken\}`[\s\n]+\}[\s\n]+\}\);",
    r"const res = await window.apiService.getWalletBalance();",
    js
)

# 7. Withdraw
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/wallet/withdraw`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{[\s\n]+'Content-Type': 'application/json',[\s\n]+'Authorization': `Bearer \$\{currentToken\}`[\s\n]+\},[\s\n]+body: JSON.stringify\(\{ payout_provider: \"paypal\", amount: 100 \}\)[\s\n]+\}\);",
    r"const res = await window.apiService.withdrawCoins('paypal', 100);",
    js
)

# 8. Update Profile (Gender Preference)
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/profile/`, \{[\s\n]+method: 'PUT',[\s\n]+headers: \{[\s\n]+'Content-Type': 'application/json',[\s\n]+'Authorization': `Bearer \$\{currentToken\}`[\s\n]+\},[\s\n]+body: JSON.stringify\(\{ gender_preference: prefGender.value \}\)[\s\n]+\}\);",
    r"const res = await window.apiService.updateProfile({ gender_preference: prefGender.value });",
    js
)

# 9. Match Random
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/match/random`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{ 'Authorization': `Bearer \$\{currentToken\}`, 'Content-Type': 'application/json' \},[\s\n]+body: JSON.stringify\(\{ medium: currentMedium \}\)[\s\n]+\}\);",
    r"const res = await window.apiService.requestRandomMatch(currentMedium);",
    js
)

# 10. Match Cancel
js = re.sub(
    r"await fetch\(`\$\{API_BASE\}/match/cancel`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{ 'Authorization': `Bearer \$\{currentToken\}` \}[\s\n]+\}\);",
    r"await window.apiService.cancelMatch();",
    js
)

# 11. Earn Coins
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/wallet/earn`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{ 'Content-Type': 'application/json', 'Authorization': `Bearer \$\{currentToken\}` \},[\s\n]+body: JSON.stringify\(\{ minutes: earnedMins, medium: earnedMedium \}\)[\s\n]+\}\);",
    r"const res = await window.apiService.earnCoins(earnedMedium, earnedMins);",
    js
)

# 12. Get Profile (Settings Modal update)
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/profile/me`, \{[\s\n]+headers: \{ 'Authorization': `Bearer \$\{currentToken\}` \}[\s\n]+\}\);",
    r"const res = await window.apiService.getProfile();",
    js
)

# 13. Update Profile (Full settings)
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/profile/`, \{[\s\n]+method: 'PUT',[\s\n]+headers: \{ 'Content-Type': 'application/json', 'Authorization': `Bearer \$\{currentToken\}` \},[\s\n]+body: JSON.stringify\(payload\)[\s\n]+\}\);",
    r"const res = await window.apiService.updateProfile(payload);",
    js
)

# 14. Upload Picture
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/profile/picture/upload`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{ 'Authorization': `Bearer \$\{currentToken\}` \},[\s\n]+body: formData[\s\n]+\}\);",
    r"const res = await window.apiService.uploadProfilePicture(formData);",
    js
)

# 15. Change Password
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/profile/password`, \{[\s\n]+method: 'PUT',[\s\n]+headers: \{ 'Content-Type': 'application/json', 'Authorization': `Bearer \$\{currentToken\}` \},[\s\n]+body: JSON.stringify\(\{[\s\n]+current_password: cp,[\s\n]+new_password: np[\s\n]+\}\)[\s\n]+\}\);",
    r"const res = await window.apiService.changePassword(cp, np);",
    js
)

# 16. Delete Account
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/profile/account/delete`, \{[\s\n]+method: 'POST',[\s\n]+headers: \{ 'Content-Type': 'application/json', 'Authorization': `Bearer \$\{currentToken\}` \},[\s\n]+body: JSON.stringify\(\{[\s\n]+current_password: delPass[\s\n]+\}\)[\s\n]+\}\);",
    r"const res = await window.apiService.deleteAccount(delPass);",
    js
)

# 17. Load 3D Studio (Get Profile again inside load3dStudio)
js = re.sub(
    r"const res = await fetch\(`\$\{API_BASE\}/profile/`, \{[\s\n]+method: 'PUT',[\s\n]+headers: \{ 'Content-Type': 'application/json', 'Authorization': `Bearer \$\{currentToken\}` \},[\s\n]+body: JSON.stringify\(\{ customizations: savedCust \}\)[\s\n]+\}\);",
    r"const res = await window.apiService.updateProfile({ customizations: savedCust });",
    js
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(js)

print("Refactoring complete.")
