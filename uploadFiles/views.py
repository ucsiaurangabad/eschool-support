from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ProfileImageForm
from .models import ProfileImage
import razorpay
from paytm import checksum
from django.views.decorators.csrf import csrf_exempt


MERCHANT_KEY = '0F#XaCuV5EisHj4Z'

def index(request):
    context = {}
    context['message'] = 'Trying ...'
    if request.method == 'POST':
        image_file = request.FILES['myFile']
        upload = ProfileImage(file = image_file)
        upload.save()
        image_url = upload.file.url
        return render(request, 'uploadFiles/index.html',{
             'image_url': image_url})

    return render(request,'uploadFiles/index.html',context)
    
      # form = ProfileImageForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()
        #     context['message'] = 'Successfully uploaded'
        #     return render(request, 'uploadFiles/index.html',context)
    
    
    # 	if form.is_valid():
    #         form.save()
    #         return render(request, 'uploadFiles/index.html')
    # return render(request,'uploadFiles/index.html')


# def image_upload(request):
#     if request.method == 'POST':
#         image_file = request.FILES['image_file']
#         image_type = request.POST['image_type']
#         if settings.USE_S3:
#             if image_type == 'private':
#                 upload = UploadPrivate(file=image_file)
#             else:
#                 upload = Upload(file=image_file)
#             upload.save()
#             image_url = upload.file.url
#         else:
#             fs = FileSystemStorage()
#             filename = fs.save(image_file.name, image_file)
#             image_url = fs.url(filename)
#         return render(request, 'upload.html', {
#             'image_url': image_url
#         })
#     return render(request, 'upload.html')

def makePayment(request):
  param_dict = {
            'MID':'dxsHEm71671540073318',
            'ORDER_ID':'01',
            'TXN_AMOUNT':'1',
            'CUST_ID':'stnms@gmail.com',
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	          'CALLBACK_URL':'http://127.0.0.1:8000/handlepayment/',
        }
  param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict,MERCHANT_KEY)
  return render(request, 'uploadFiles/paytm.html', {'param_dict' : param_dict})








#     client = razorpay.Client(auth=("rzp_test_6Bs3UVYO7AaMsS", "ahUwl7gxSkXawFb7SaFRZNGb"))
    
#     DATA = {}
#     DATA:{
#             'amount'           :5000,
#             'currency'         :'INR',
#             'receipt'          : 'rcptid123',
#             'payment_capture'  : 0}

#     client.order.create(data=DATA)

    
#     # client = razorpay.Client(auth=("rzp_test_6Bs3UVYO7AaMsS", "ahUwl7gxSkXawFb7SaFRZNGb"))
#     # order_amount = 50000 
#     # order_currency = 'INR'
#     # order_receipt = 'order_rcptid_11'
#     # notes = {'Shipping address': 'Bommanahalli, Bangalore'}   
#     # client.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0')
    
@csrf_exempt 
def handlepayment(request):
  form = request.POST
  response_dict = {}
  for i in form.keys():
    response_dict[i] = form[i]
    if i == 'CHECKSUMHASH':
      CheckSum = form[i]

  verify = checksum.verify_checksum(response_dict,MERCHANT_KEY,CheckSum)

  if verify:
    if response_dict['RESPCODE'] == '01':
      print('order successful')
    else:
      print('order was not successful because' + response_dict['RESPMSG'])
  return render(request, 'uploadFiles/paymentstatus.html', {'response': response_dict})