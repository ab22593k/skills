# Session-Based Test Management (SBTM) Session Report

## Session Metadata
- **Charter**: Explore the URL validation and error handling for malformed inputs
- **Tester**: [Your Name]
- **Date**: 2026-01-31
- **Session Duration**: 90 minutes
- **Start Time**: 10:00 AM
- **End Time**: 11:30 AM

## Areas Explored
1. URL input validation on the creation form
2. Error messages displayed to users
3. Backend API validation logic
4. Edge cases with international domains
5. Behavior with extremely long URLs

## Bugs Found
### BUG-2026-001: Application crashes on URL with null bytes
- **Severity**: High
- **Status**: Filed
- **Summary**: Submitting a URL containing `%00` (null byte) causes 500 error instead of validation message
- **Oracle Used**: World (should handle invalid input gracefully), Purpose (input validation should catch this)

### BUG-2026-002: Inconsistent error messaging for invalid protocols
- **Severity**: Low
- **Status**: Filed
- **Summary**: FTP URLs show "Invalid URL" but mailto: URLs show "Protocol not supported" - inconsistent user experience
- **Oracle Used**: Comparable Products (other shorteners use consistent messaging), User Expectations

### BUG-2026-003: No validation feedback during paste operation
- **Severity**: Medium
- **Status**: Filed
- **Summary**: When pasting a very long URL (>5000 chars), no immediate feedback; user must click "Shorten" to see error
- **Oracle Used**: Usability, User Expectations

## Test Notes (Chronological Log)

**10:00-10:15** - Started with basic validation testing. Tested obvious cases: empty string, plain text, URLs without protocols. All returned appropriate error messages. Frontend validation working as expected.

**10:15-10:30** - Moved to protocol testing. HTTP/HTTPS work fine. FTP URLs are rejected (expected). Discovered BUG-2026-002: mailto: and tel: URLs give different error messages. This seems like an inconsistency in the validation logic.

**10:30-10:45** - Testing special characters. Ampersands, question marks, hashes all work correctly (properly encoded). **Found BUG-2026-001**: Null byte (`%00`) caused a 500 Internal Server Error! Checked server logs - unhandled exception in the URL parsing library. This is a security concern.

**10:45-11:00** - Investigating the null byte issue further. Tried other control characters:
- `%01`-`%1F`: All handled gracefully (rejected with "Invalid URL")
- `%7F`: Handled correctly
- Only `%00` causes crash - seems like a specific null termination issue

**11:00-11:15** - Testing long URLs. Created test cases:
- 1,000 chars: Works fine
- 5,000 chars: Works fine
- 10,000 chars: Returns "URL too long" (good!)
- **BUG-2026-003**: No real-time feedback; user has to submit to find out

**11:15-11:30** - International domain names. Tested:
- Chinese characters: Works (properly punycoded)
- Arabic characters: Works
- Emoji in URL: Rejected (reasonable)
- Mixed scripts: Works

**Final Thoughts**: The validation is mostly solid, but the null byte crash is serious. The inconsistency in error messages is a UX issue. Long URL handling could be more user-friendly.

## New Ideas for Future Testing
1. Test URL redirect loops (what if someone tries to shorten a URL that points to the shortener itself?)
2. Investigate rate limiting - can I spam the API?
3. Check if there's XSS vulnerability in the error messages
4. Test with URL shortener blacklists (some services maintain lists of blocked domains)
5. Explore analytics manipulation - can I inflate click counts?

## Obstacles Encountered
- No test data generator for edge case URLs; had to manually craft test cases
- Server logs not easily accessible in staging environment (had to ask dev for help)

## Outlook
- Need to follow up on the null byte bug - this is a security issue
- Should test the redirect functionality next (separate session)
- Want to explore the analytics feature for manipulation vulnerabilities
- Consider automation for regression testing on URL validation

## Professional Assessment
**Confidence Level**: High for validation logic (except null byte case)  
**Risk Level**: Medium (the crash is serious but requires specific input)  
**Recommendation**: Fix BUG-2026-001 before production release; other bugs can be deferred

---
*Session debriefed with: [Manager/Team Lead Name]*  
*Debrief duration: 15 minutes*
