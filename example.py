#!/usr/bin/env python3
import asyncio
import os
import time

from dotenv import load_dotenv

from monarchmoney import MonarchMoney, RequireMFAException, RateLimitError


async def main():
    try:
        # Check if .env file exists
        if os.path.isfile(".env"):
            # Load environment variables from the .env file
            load_dotenv()

        # Get environment variables
        MONARCH_EMAIL = os.getenv("MONARCH_EMAIL")
        MONARCH_PASS = os.getenv("MONARCH_PASS")
        MONARCH_MFA = os.getenv("MONARCH_MFA")

        # Check if required environment variables are set
        if not all([MONARCH_EMAIL, MONARCH_PASS]):
            print(
                "Error: MONARCH_EMAIL and MONARCH_PASS must be set in environment variables"
            )
            return 1

        # Initialize MonarchMoney
        mm = MonarchMoney()

        # Try to use saved session first, fall back to fresh login if needed
        login_successful = False
        max_rate_limit_retries = 3
        
        for attempt in range(max_rate_limit_retries):
            try:
                # First try to use saved session
                await mm.login(
                    email=MONARCH_EMAIL,
                    password=MONARCH_PASS,
                    save_session=True,
                    use_saved_session=True,
                    mfa_secret_key=MONARCH_MFA,
                )
                print("✅ Successfully logged in using saved session")
                login_successful = True
                break
                
            except RateLimitError as rate_error:
                print(f"⚠️  Rate limited (attempt {attempt + 1}/{max_rate_limit_retries}): {rate_error}")
                if attempt < max_rate_limit_retries - 1:
                    wait_time = 60 * (2 ** attempt)  # 60s, 120s, 240s
                    print(f"🕒 Waiting {wait_time} seconds before retry...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    print("❌ Rate limit exceeded maximum retries. Please try again later (15-30 minutes).")
                    return 1
                    
            except Exception as session_error:
                print(f"⚠️  Saved session failed ({session_error}), attempting fresh login...")
                try:
                    # If saved session fails, try fresh login
                    await mm.login(
                        email=MONARCH_EMAIL,
                        password=MONARCH_PASS,
                        save_session=True,
                        use_saved_session=False,
                        mfa_secret_key=MONARCH_MFA,
                    )
                    print("✅ Successfully logged in with fresh authentication")
                    login_successful = True
                    break
                except RateLimitError as rate_error:
                    print(f"⚠️  Fresh login also rate limited (attempt {attempt + 1}/{max_rate_limit_retries}): {rate_error}")
                    if attempt < max_rate_limit_retries - 1:
                        wait_time = 60 * (2 ** attempt)  # 60s, 120s, 240s
                        print(f"🕒 Waiting {wait_time} seconds before retry...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print("❌ Rate limit exceeded maximum retries. Please try again later (15-30 minutes).")
                        return 1
        
        if not login_successful:
            print("❌ Failed to login after all attempts")
            return 1

        # Get accounts
        accounts_response = await mm.get_accounts()
        accounts = accounts_response['accounts']
        print(f"Successfully retrieved {len(accounts)} accounts")

        return 0  # Indicate successful execution

    except RequireMFAException as e:
        print(f"MFA required: {e}")
        print("Please check your MFA secret key in the .env file")
        return 1
    except RateLimitError as e:
        print(f"Rate limit error: {e}")
        print("""
🚨 RATE LIMIT TROUBLESHOOTING:
1. You've made too many login attempts recently
2. Wait 15-30 minutes before trying again  
3. Check if you have a valid saved session: temp_session.json
4. Consider using saved sessions instead of fresh logins
5. Avoid running multiple instances simultaneously
        """)
        return 1
    except Exception as e:
        print(f"Error condition: {e}")
        if "429" in str(e) or "rate limit" in str(e).lower():
            print("""
🚨 RATE LIMIT DETECTED:
This appears to be a rate limiting issue. Please:
1. Wait 15-30 minutes before trying again
2. Use saved sessions when possible (set use_saved_session=True)
3. Avoid rapid successive login attempts
            """)
        return 1  # Indicate error


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    if exit_code == 0:
        print("Main completed successfully.")
    else:
        print("Main failed to complete.")
