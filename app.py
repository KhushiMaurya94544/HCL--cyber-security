from flask import Flask, render_template, request
import random
import time

app = Flask(__name__)

# Temporary OTP storage
otp_store = {}

# Demo login details
USERNAME = "admin"
PASSWORD = "1234"


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""
    status = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        otp = request.form.get("otp", "").strip()

        # Generate OTP
        if "generate" in request.form:

            if username == USERNAME and password == PASSWORD:

                generated_otp = str(random.randint(100000, 999999))

                otp_store[username] = {
                    "code": generated_otp,
                    "time": time.time()
                }

                print("\n==========================")
                print(" TWO STEP VERIFICATION")
                print("==========================")
                print("Username:", username)
                print("Your OTP is:", generated_otp)
                print("==========================\n")

                message = "OTP generated successfully! Check Terminal."
                status = "success"

            else:
                message = "Invalid Username or Password!"
                status = "error"

        # Verify OTP
        elif "verify" in request.form:

            saved_otp = otp_store.get(username)

            if saved_otp:

                time_difference = time.time() - saved_otp["time"]

                if time_difference > 120:
                    otp_store.pop(username, None)
                    message = "OTP Expired! Generate a new OTP."
                    status = "error"

                elif otp == saved_otp["code"] and otp != "":
                    otp_store.pop(username, None)

                    message = "LOGIN SUCCESSFUL! Welcome " + username
                    status = "success"

                else:
                    message = "Incorrect OTP! Please try again."
                    status = "error"

            else:
                message = "Please generate OTP first!"
                status = "error"

    return render_template(
        "index.html",
        message=message,
        status=status
    )


if __name__ == "__main__":

    print("Starting Two Step Verification System...")
    print("Open: http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )