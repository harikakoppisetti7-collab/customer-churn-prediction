import streamlit as st
import pandas as pd
import joblib


# ==================================================
# LOAD TRAINED MODEL
# ==================================================

model = joblib.load("churn_model.pkl")


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Customer Retention Intelligence",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("🤖 Customer Retention Intelligence System")

st.write(
    "Predict customer churn, estimate risk, "
    "understand risk factors, and recommend "
    "personalized retention actions."
)


# ==================================================
# CUSTOMER INFORMATION
# ==================================================

st.header("👤 Customer Information")

col1, col2 = st.columns(2)


# ==================================================
# LEFT COLUMN
# ==================================================

with col1:

    customer_id = st.text_input(
        "Customer ID",
        "CUST001"
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        [0, 1]
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

    tenure = st.number_input(
        "Tenure (Months)",
        min_value=0,
        max_value=100,
        value=12
    )

    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["Yes", "No", "No phone service"]
    )

    online_security = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"]
    )


# ==================================================
# RIGHT COLUMN
# ==================================================

with col2:

    device_protection = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"]
    )

    tech_support = st.selectbox(
        "Tech Support",
        ["Yes", "No", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"]
    )

    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    contract = st.selectbox(
        "Contract",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=50.0
    )

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=500.0
    )


# ==================================================
# ANALYZE BUTTON
# ==================================================

st.divider()

analyze = st.button(
    "🔮 ANALYZE CUSTOMER",
    use_container_width=True
)


# ==================================================
# ANALYSIS
# ==================================================

if analyze:

    # ------------------------------------------------
    # CREATE CUSTOMER DATA
    # ------------------------------------------------

    customer_data = pd.DataFrame({

        "gender": [gender],

        "SeniorCitizen": [senior_citizen],

        "Partner": [partner],

        "Dependents": [dependents],

        "tenure": [tenure],

        "PhoneService": [phone_service],

        "MultipleLines": [multiple_lines],

        "InternetService": [internet_service],

        "OnlineSecurity": [online_security],

        "OnlineBackup": [online_backup],

        "DeviceProtection": [device_protection],

        "TechSupport": [tech_support],

        "StreamingTV": [streaming_tv],

        "StreamingMovies": [streaming_movies],

        "Contract": [contract],

        "PaperlessBilling": [paperless_billing],

        "PaymentMethod": [payment_method],

        "MonthlyCharges": [monthly_charges],

        "TotalCharges": [total_charges]
    })


    # ------------------------------------------------
    # MODEL PREDICTION
    # ------------------------------------------------

    prediction = model.predict(customer_data)[0]

    probability = model.predict_proba(
        customer_data
    )[0][1]


    # ------------------------------------------------
    # RISK LEVEL
    # ------------------------------------------------

    if probability < 0.30:

        risk_level = "LOW"

    elif probability < 0.70:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    # ------------------------------------------------
    # CHURN RISK
    # ------------------------------------------------

    st.subheader("📈 Churn Risk")

    risk_col1, risk_col2 = st.columns(2)

    with risk_col1:

        st.metric(
            "Churn Probability",
            f"{probability * 100:.2f}%"
        )

    with risk_col2:

        st.metric(
            "Risk Level",
            risk_level
        )


    # ------------------------------------------------
    # CHURN RESULT
    # ------------------------------------------------

    if prediction == 1:

        st.error(
            "⚠️ Customer is likely to CHURN"
        )

    else:

        st.success(
            "✅ Customer is likely to STAY"
        )


    # ------------------------------------------------
    # CUSTOMER VALUE
    # ------------------------------------------------

    if monthly_charges >= 70 and probability >= 0.50:

        customer_value = "HIGH-VALUE AT RISK"

    elif monthly_charges >= 50:

        customer_value = "MEDIUM-VALUE"

    else:

        customer_value = "STANDARD"


    st.subheader("💰 Customer Value")

    st.info(
        f"Customer Segment: {customer_value}"
    )


    # ------------------------------------------------
    # RISK FACTORS
    # ------------------------------------------------

    reasons = []


    if contract == "Month-to-month":

        reasons.append(
            "Customer has a month-to-month contract."
        )


    if monthly_charges > 70:

        reasons.append(
            "Customer has relatively high monthly charges."
        )


    if tenure < 12:

        reasons.append(
            "Customer has relatively low tenure."
        )


    if payment_method == "Electronic check":

        reasons.append(
            "Customer uses electronic check payment."
        )


    if internet_service == "Fiber optic":

        reasons.append(
            "Customer uses fiber optic internet service."
        )


    if online_security == "No":

        reasons.append(
            "Customer does not have online security."
        )


    if tech_support == "No":

        reasons.append(
            "Customer does not have technical support."
        )


    # ------------------------------------------------
    # DISPLAY RISK FACTORS
    # ------------------------------------------------

    st.subheader("🔍 Risk Factors")


    if reasons:

        for reason in reasons:

            st.warning(
                "⚠️ " + reason
            )

    else:

        st.success(
            "No major risk factors identified."
        )


    # ------------------------------------------------
    # RETENTION RECOMMENDATION
    # ------------------------------------------------

    st.subheader(
        "🎯 Recommended Retention Action"
    )


    if probability >= 0.70:

        if contract == "Month-to-month":

            recommendation = (
                "Offer a discounted long-term contract "
                "with loyalty benefits."
            )

        elif monthly_charges > 70:

            recommendation = (
                "Offer a personalized pricing plan "
                "or service bundle."
            )

        elif tenure < 12:

            recommendation = (
                "Provide a new-customer loyalty offer "
                "and onboarding support."
            )

        else:

            recommendation = (
                "Prioritize the customer for a "
                "personalized retention campaign."
            )


    elif probability >= 0.30:

        recommendation = (
            "Monitor the customer and provide "
            "targeted engagement offers."
        )


    else:

        recommendation = (
            "No immediate retention intervention required."
        )


    # ------------------------------------------------
    # DISPLAY RECOMMENDATION
    # ------------------------------------------------

    st.info(
        "💡 " + recommendation
    )


    # ------------------------------------------------
    # CUSTOMER SUMMARY
    # ------------------------------------------------

    st.subheader("📋 Customer Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:

        st.write("**Customer ID:**", customer_id)

        st.write("**Gender:**", gender)

        st.write("**Tenure:**", f"{tenure} months")


    with summary_col2:

        st.write(
            "**Monthly Charges:**",
            f"${monthly_charges:.2f}"
        )

        st.write(
            "**Total Charges:**",
            f"${total_charges:.2f}"
        )

        st.write(
            "**Contract:**",
            contract
        )


    with summary_col3:

        st.write(
            "**Internet Service:**",
            internet_service
        )

        st.write(
            "**Payment Method:**",
            payment_method
        )

        st.write(
            "**Customer Value:**",
            customer_value
        )