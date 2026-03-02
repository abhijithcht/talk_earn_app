# Talk & Earn — Database Architecture

This document maps the core database schema (defined in `app/models.py` via SQLAlchemy) to the business rules outlined in the **Talk & Earn Platform Concept**.

---

## 1. Users & Compliance (`users` table)

The `User` model is the core of the application, managing authentication, profiles, and compliance.

### Profile & Positioning
- **Not a Dating App**: Focuses on professional, part-time earning opportunities.
- **Gender & Preferences**: Stores `gender` and `gender_preference` (Male, Female, Any) to facilitate comfortable, non-dating-focused matchmaking.
- **Avatars**: Users can select from default avatars (`avatar_id`) encompassing neutral, gender-specific, cultural, and fun categories. They can also customize colors and accessories (`customizations` JSON).

### Verification & Compliance
- **ID Verification**: Users must verify their ID (for Age Verification only, matching against `date_of_birth`).
- **Face Verification**: Ensures the user matches their ID via selfie match.
- **Status Flag**: `verification_status` tracks progression (`pending`, `verified`, `rejected`).
- **Data Safety**: Only stores an `id_hash` rather than raw documents for privacy and compliance.

---

## 2. Wallet & Earnings (`wallets` & `transactions` tables)

The platform operates on a coin-based part-time earning model.

- **Earn Rate**: Users earn coins per minute of communication based on the medium (Text, Audio, Video).
- **Exchange Rate**: 100 coins = $1.00 USD.
- **Withdrawal Rules**: The minimum withdrawal threshold is 100 coins. If a user's rating drops below 3 stars, `withdrawal_blocked` is flagged to `True` on their `User` record.
- **Payout Providers**: Payouts are facilitated securely to linked `stripe_account_id` or PayPal accounts, tracked via `payout_provider` in the `transactions` table.

---

## 3. Communication Sessions (`sessions` table)

Tracks all random matches and connections made through the platform.

- **End-to-End Encryption**: The actual stream data (WebRTC audio/video and WebSocket text) is encrypted end-to-end and is **never** stored in the database.
- **Session Records**: The database only stores metadata (`caller_id`, `callee_id`, `session_type`, `duration_minutes`) to facilitate coin payouts and post-session ratings.
- **Post-Session Ratings**: Users rate each other from 1 to 5 stars (`rating` column).

---

## 4. Quality Control & Moderation (`warnings`, `audit_logs`, `banned_ids`)

The platform emphasizes safety and scam prevention via AI filters and active moderation.

### Ratings Impact
- **>= 4 Stars**: High ratings grant normal earnings + a potential algorithmic bonus.
- **3 Stars**: Medium ratings flag the user's account for manual moderator review.
- **< 3 Stars**: Low ratings automatically block withdrawals (`withdrawal_blocked=True`).

### Warning System (3-Strike Rule)
Moderation actions are recorded in the `warnings` table (`user_id`, `level`, `reason`).
1. **Level 1**: First Reminder
2. **Level 2**: Account Freeze
3. **Level 3**: Permanent Ban

### Audit & Blacklist
- **Audit Logs**: The `audit_logs` table provides a secure history of all moderator actions (`admin_id`, `action`, `target_user_id`) to ensure transparency and accountability.
- **Banned IDs**: If a user hits a Level 3 Ban, their hardware/document hash is permanently added to the `banned_ids` table to prevent platform re-entry.

---

## 5. Follows (`follows` table)
Users can send "Follow Requests" after a session to easily reconnect with good conversationalists, tracked via the `follower_id` and `followed_id` relationships.
