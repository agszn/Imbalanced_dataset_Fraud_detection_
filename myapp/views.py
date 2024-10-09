from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *
from .models import *
from django.db.models import Q

from django.http import JsonResponse
from django.conf import settings
import os

import joblib
import numpy as np

def base(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about/about.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new registration object and avoid saving it yet
            new_user = user_form.save(commit=False)
            #reset the choosen password
            new_user.set_password(user_form.cleaned_data['password'])
            #save the new registration
            new_user.save()
            return render(request, 'registration/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html',{'user_form':user_form})

def profile(request):
    return render(request, 'profile/profile.html')



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user = user_form.save()
            profile = user.profile
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        user_form = EditProfileForm(instance=request.user)
    
    return render(request, 'profile/edit_profile.html', {'user_form': user_form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account was successfully deleted.')
        return redirect('base')  # Redirect to the homepage or another page after deletion

    return render(request, 'registration/delete_account.html')
# das
@login_required
def dashboard(request):
    users_count = User.objects.all().count()
    consumers = Consumer.objects.all().count

    context = {
        'users_count':users_count,
        'consumers':consumers,
    }
    return render(request, "dashboard/dashboard.html", context=context)


# Contact start
@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us!")
            return redirect('dashboard')  # Redirect to the same page to show the modal
    else:
        form = ContactForm()

    return render(request, 'contact/contact_form.html', {'form': form})

# contact end
from django.shortcuts import render
import joblib
import numpy as np

# Load the saved model
model = joblib.load('models/fraud_detection_model.pkl')

def fraud_prediction(request):
    if request.method == 'POST':
        # Get input data from the form
        amount = float(request.POST.get('amount'))
        time = float(request.POST.get('time'))
        
        # Get the V1 to V28 values from the form
        v_values = [float(request.POST.get(f'v{i}')) for i in range(1, 29)]

        # Prepare data for prediction
        data = np.array([[time, *v_values, amount]])

        # Predict using the loaded model
        prediction = model.predict(data)
        
        # Prepare a human-readable response
        result = "Fraudulent Transaction" if prediction == 1 else "Non-Fraudulent Transaction"

        return render(request, 'predictor/predict.html', {'result': result, 'range': range(1, 29)})
    
    # Pass the range to the template
    return render(request, 'predictor/predict.html', {'range': range(1, 29)})

# views.py
from django.shortcuts import render
import pandas as pd

# views.py
from django.shortcuts import render
import pandas as pd


def dataset(request):
    # Load your dataset
    df = pd.read_csv('models/creditcard.csv')  # Adjust the path to your dataset

    # Separate the fraudulent and non-fraudulent transactions
    df_fraud = df[df['Class'] == 1]  # Assuming 'Class' column indicates fraud (1) or not (0)
    df_non_fraud = df[df['Class'] == 0]

    # Get the number of rows to display
    fraud_rows = df_fraud.head(10)  # Get top 10 fraudulent transactions
    non_fraud_rows = df_non_fraud.head(10)  # Get top 10 non-fraudulent transactions

    # Concatenate the two DataFrames
    df_combined = pd.concat([fraud_rows, non_fraud_rows])

    # Convert the combined DataFrame to HTML
    dataset_html = df_combined.to_html(classes='table table-striped', index=False)

    return render(request, 'dataset/dataset.html', {
        'dataset': dataset_html,
    })

# views.py
from django.shortcuts import render
import os
from django.conf import settings

def image_gallery(request):
    # Path to the image directory inside static files
    image_dir = os.path.join(settings.STATICFILES_DIRS[0], 'graphs')

    # List of image file names
    images = [img for img in os.listdir(image_dir) if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    return render(request, 'graphs/graph.html', {'images': images})


from django.shortcuts import render
from .forms import TransactionForm
from .models import Transaction

def fraud_detection_logic(transaction):
    """
    Simple rule-based fraud detection logic.
    Modify this based on your specific requirements.
    """
    # Rule 1: Check if the transaction amount exceeds a certain threshold
    if transaction.transaction_amount > 5000:
        return True  # Fraudulent transaction

    # Rule 2: Check if the merchant type or location is unusual (customize as needed)
    suspicious_merchants = ['electronics', 'luxury items', 'online casino']  # Example of suspicious merchant types
    if transaction.merchant_type.lower() in suspicious_merchants:
        return True  # Fraudulent transaction

    # Rule 3: Check if the transaction is happening in an unusual location
    suspicious_locations = ['international', 'remote locations']
    if transaction.location.lower() in suspicious_locations:
        return True  # Fraudulent transaction

    # If no rules are triggered, the transaction is considered non-fraudulent
    return False

def fraud_prediction_val(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # Save the transaction details to the database but don't commit yet
            transaction = form.save(commit=False)

            # Apply fraud detection logic
            is_fraudulent = fraud_detection_logic(transaction)

            # Update the transaction with the fraud status
            transaction.is_fraudulent = is_fraudulent
            transaction.save()

            # Prepare the result message
            result = "Fraudulent Transaction" if is_fraudulent else "Non-Fraudulent Transaction"

            # Render the result page
            return render(request, 'value/result.html', {'result': result, 'transaction': transaction})
    else:
        form = TransactionForm()

    return render(request, 'value/predict.html', {'form': form})
