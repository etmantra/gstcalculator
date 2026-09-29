from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def gst_calculator():
    result = None
    form_data = {}  # Dictionary to remember user inputs
    
    if request.method == "POST":
        try:
            # Retrieve form data
            amount = float(request.form.get("amount", 0))
            tax_type = request.form.get("tax_type") 
            gst_rate = float(request.form.get("gst_rate", 0))

            # Store the inputs to pass back to the HTML form
            form_data = {
                "amount": request.form.get("amount", ""),
                "tax_type": tax_type,
                "gst_rate": int(gst_rate)
            }

            # Calculate GST based on inclusive or exclusive selection
            if tax_type == "exclusive":
                base_price = amount
                total_gst = amount * (gst_rate / 100)
                total_price = amount + total_gst
            elif tax_type == "inclusive":
                base_price = amount / (1 + (gst_rate / 100))
                total_gst = amount - base_price
                total_price = amount

            # Split into CGST and SGST
            cgst = total_gst / 2
            sgst = total_gst / 2

            # Package results for the template
            result = {
                "base_price": round(base_price, 2),
                "cgst": round(cgst, 2),
                "sgst": round(sgst, 2),
                "total_gst": round(total_gst, 2),
                "total_price": round(total_price, 2),
                "rate": int(gst_rate)
            }
        except ValueError:
            pass

    return render_template("index.html", result=result, form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True)