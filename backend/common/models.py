import hmac
import hashlib
import json
import time
from django.db import models
from django.conf import settings
from account import models as acc_models
from operation import models as op_models
from django.conf import settings
# Create your models here.


# Secret key for checksum generation
CHECKSUM_KEY =  settings.PG_PARAMS['salt']
RU = settings.PG_PARAMS['return_url']


class PaymentTransaction(models.Model):
    application= models.BigIntegerField()
    application_no= models.CharField(max_length=50, null=False)
    application_generation = models.CharField(
        max_length=20,
        choices=[('NEW', 'New'), ('OLD', 'Old'),],
        default='NEW'
    )
    # Common Fields
    merchant_id = models.CharField(max_length=50)  # BillDesk Merchant ID
    order_id = models.CharField(max_length=50, unique=True)  # Unique Order ID
    txn_reference_no = models.CharField(max_length=50, blank=True, null=True)  # BillDesk Transaction Reference Number
    bank_reference_no = models.CharField(max_length=50, blank=True, null=True)  # Bank Reference Number
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Transaction amount
    currency_name = models.CharField(max_length=10, default="INR")  # Currency (e.g., INR)
    txn_type = models.CharField(max_length=50, blank=True, null=True)  # Type of transaction
    txn_date = models.DateTimeField(blank=True, null=True)  # Date and time of transaction
    status = models.CharField(
        max_length=20,
        choices=[('INITIATED', 'Initiated'), ('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')],
        default='INITIATED'
    )  # Payment status

    # Security Details
    security_id = models.CharField(max_length=50, blank=True, null=True)  # Security ID
    security_password = models.CharField(max_length=50, blank=True, null=True)  # Security Password
    security_type = models.CharField(max_length=50, blank=True, null=True)  # Security Type
   
    # Bank & Payment Details
    ibank_id = models.CharField(max_length=50, blank=True, null=True)  # Internet Banking ID
    bank_merchant_id = models.CharField(max_length=50, blank=True, null=True)  # Bank Merchant ID
    
    # Transaction Metadata
    item_code = models.CharField(max_length=50, blank=True, null=True)  # Item code for purchase
    auth_status = models.CharField(max_length=50, blank=True, null=True)  # Authorization status
    settlement_type = models.CharField(max_length=50, blank=True, null=True)  # Settlement Type

    # Additional Information Fields (txtadditional fields)
    additional_info1 = models.CharField(max_length=255, blank=True, null=True)
    additional_info2 = models.CharField(max_length=255, blank=True, null=True)
    additional_info3 = models.CharField(max_length=255, blank=True, null=True)
    additional_info4 = models.CharField(max_length=255, blank=True, null=True)
    additional_info5 = models.CharField(max_length=255, blank=True, null=True)
    additional_info6 = models.CharField(max_length=255, blank=True, null=True)
    additional_info7 = models.CharField(max_length=255, blank=True, null=True)

    # Reserved Fields
    na1 = models.CharField(max_length=50, default="NA")
    na2 = models.CharField(max_length=50, default="NA")
    na3 = models.CharField(max_length=50, default="NA")
    na4 = models.CharField(max_length=50, default="NA")
    na5 = models.CharField(max_length=50, default="NA")
    na6 = models.CharField(max_length=50, default="NA")
    na7 = models.CharField(max_length=50, default="NA")

    type_field1= models.CharField(max_length=50, default="R")
    type_field2= models.CharField(max_length=50, default="F")

    # Error Handling
    error_status = models.CharField(max_length=50, blank=True, null=True)  # Error status
    error_description = models.TextField(blank=True, null=True)  # Description of error (if any)

    # Checksum for Security
    checksum = models.CharField(max_length=100)  # Checksum for security validation

    # Request and Response Tracking
    request_payload = models.TextField(blank=True, null=True)  # Store raw request data
    response_payload = models.TextField(blank=True, null=True)  # Store raw response data
    created_by = models.ForeignKey(acc_models.User, null=True, on_delete=models.SET_NULL, related_name="payment_created_by") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(acc_models.User, null=True, on_delete=models.SET_NULL, related_name="payment_updated_by") 
    updated_at = models.DateTimeField(auto_now = True)

#     Request:
# MerchantID | CustomerID | NA | TxnAmount |NA | NA | NA | CurrencyType | NA | TypeFieId1 | SecurityID |
#  NA | NA | TypeField2 | txtadditional1 | 	txtadditional2 | txtadditional3 | txtadditional4 | txtadditional5 |
#  txtadditional6 | txtadditional7 | RU


    
    def generate_checksum(self, raw_string):
        """
        Generates checksum for security
        """
        # raw_string = f"{self.merchant_id}|{self.order_id}|{self.na1}|{self.amount}|{self.na2}|{self.na3}|{self.na4}|{self.currency_name}|{self.na5}|{self.type_field1}|{self.security_id}|" \
        #              f"{self.na6}|{self.na7}|{self.type_field2}|{self.additional_info1}|{self.additional_info2}|{self.additional_info3}|{self.additional_info4}|{self.additional_info5}|"\
        #              f"{self.additional_info6}|{self.additional_info7}|{RU}|{CHECKSUM_KEY}"
        
         # Encode the input string and key as bytes
        input_bytes = raw_string.encode('utf-8')
        key_bytes = CHECKSUM_KEY.encode('utf-8')
        
        # Create an HMAC object using SHA-256
        hmac_hash = hmac.new(key_bytes, input_bytes, hashlib.sha256)
    
        # Get the hexadecimal representation of the hash
        checksum = hmac_hash.hexdigest()
        return checksum.upper()

        # return hashlib.sha256(raw_string.encode()).hexdigest()

    def verify_checksum(self, msg):
        """
        Verifies checksum from BillDesk response
        """
        # Response:
        # MerchantID | CustomerID | TxnReferenceNo | BankReferenceNo | TxnAmount IBankID |
        # BankMerchantID | TxnType | CurrencyName | ItemCode | SecurityType | SecurityID | 
        # SecurityPassword | TxnDate | AuthStatus | SettlementType | AdditionalInfo1 | Additionallnfo2 |
        # AdditionalInfo3|Additionallnfo4 | AdditionalInfo5 |AdditionalInfo6 | Additionallnfo7 | 
        # ErrorStatus | ErrorDescription | CheckSum
        # 
        # Split the message into parts
        msg_parts = msg.split("|")

        # Remove the last element (checksum)
        msg_without_checksum = "|".join(msg_parts[:-1])

        print("raw_string:",msg_without_checksum)
        
        input_bytes = msg_without_checksum.encode('utf-8')
        key_bytes = CHECKSUM_KEY.encode('utf-8')
        
        # Create an HMAC object using SHA-256
        hmac_hash = hmac.new(key_bytes, input_bytes, hashlib.sha256)
    
        # Get the hexadecimal representation of the hash
        checksum = hmac_hash.hexdigest().upper()
        print("Generatred Check_sum", checksum)
        return checksum == msg_parts[-1]

    def __str__(self):
        return f"Order {self.order_id} - Status: {self.status}"




# class BillDeskOrderTransaction(models.Model):
#     # Order Details
#     mercid = models.CharField(max_length=50, help_text="Merchant ID")
#     orderid = models.CharField(max_length=50, unique=True, help_text="Order ID")
#     amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Order Amount")
#     order_date = models.DateTimeField(help_text="Order Date and Time")
#     currency = models.CharField(max_length=10, help_text="Currency Code")
#     ru = models.URLField(max_length=255, help_text="Return URL")
#     itemcode = models.CharField(max_length=50, help_text="Item Code")

#     # Additional Info
#     additional_info1 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 1")
#     additional_info2 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 2")

#     # Invoice Details
#     invoice_number = models.CharField(max_length=50, blank=True, null=True, help_text="Invoice Number")
#     invoice_display_number = models.CharField(max_length=50, blank=True, null=True, help_text="Invoice Display Number")
#     customer_name = models.CharField(max_length=100, blank=True, null=True, help_text="Customer Name")
#     invoice_date = models.DateTimeField(blank=True, null=True, help_text="Invoice Date")

#     # GST Details
#     gst_cgst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="CGST Amount")
#     gst_sgst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="SGST Amount")
#     gst_igst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="IGST Amount")
#     gst_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Total GST Amount")
#     gst_cess = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="GST CESS Amount")
#     gst_incentive = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="GST Incentive")
#     gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="GST Percentage")
#     gstin = models.CharField(max_length=50, blank=True, null=True, help_text="GSTIN Number")

#     # Device Details
#     device_init_channel = models.CharField(max_length=50, blank=True, null=True, help_text="Device Init Channel")
#     device_ip = models.GenericIPAddressField(blank=True, null=True, help_text="Customer IP Address")
#     device_user_agent = models.TextField(blank=True, null=True, help_text="User Agent")
#     device_accept_header = models.CharField(max_length=255, blank=True, null=True, help_text="Accept Header")
#     device_fingerprintid = models.CharField(max_length=255, blank=True, null=True, help_text="Fingerprint ID")
#     device_browser_tz = models.CharField(max_length=10, blank=True, null=True, help_text="Browser Timezone")
#     device_browser_color_depth = models.CharField(max_length=10, blank=True, null=True, help_text="Browser Color Depth")
#     device_browser_java_enabled = models.BooleanField(default=False, help_text="Java Enabled")
#     device_browser_screen_height = models.PositiveIntegerField(blank=True, null=True, help_text="Screen Height")
#     device_browser_screen_width = models.PositiveIntegerField(blank=True, null=True, help_text="Screen Width")
#     device_browser_language = models.CharField(max_length=20, blank=True, null=True, help_text="Browser Language")
#     device_browser_javascript_enabled = models.BooleanField(default=True, help_text="JavaScript Enabled")
    
#     created_by = models.ForeignKey(acc_models.User, null=True, on_delete=models.SET_NULL, related_name="payment_created_by") 
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_by = models.ForeignKey(acc_models.User, null=True, on_delete=models.SET_NULL, related_name="payment_updated_by") 
#     updated_at = models.DateTimeField(auto_now = True)
#     def __str__(self):
#         return f"Order {self.orderid} - {self.amount} {self.currency}"


# class BillDeskOrderTransactionResponse(models.Model):
#     # Order Details
#     objectid = models.CharField(max_length=50, help_text="Object ID (e.g., order)")
#     orderid = models.CharField(max_length=50, unique=True, help_text="Order ID")
#     bdorderid = models.CharField(max_length=50, unique=True, help_text="BillDesk Order ID")
#     mercid = models.CharField(max_length=50, help_text="Merchant ID")
#     order_date = models.DateTimeField(help_text="Order Date and Time")
#     amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Order Amount")
#     currency = models.CharField(max_length=10, help_text="Currency Code")
#     ru = models.URLField(max_length=255, help_text="Return URL")
#     itemcode = models.CharField(max_length=50, help_text="Item Code")
#     createdon = models.DateTimeField(help_text="Order Creation Date")
#     next_step = models.CharField(max_length=50, help_text="Next Step (e.g., redirect)")
#     status = models.CharField(max_length=20, help_text="Order Status")

#     # Additional Info
#     additional_info1 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 1")
#     additional_info2 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 2")

#     # Invoice Details
#     invoice_number = models.CharField(max_length=50, blank=True, null=True, help_text="Invoice Number")
#     invoice_display_number = models.CharField(max_length=50, blank=True, null=True, help_text="Invoice Display Number")
#     invoice_date = models.DateTimeField(blank=True, null=True, help_text="Invoice Date")
#     customer_name = models.CharField(max_length=100, blank=True, null=True, help_text="Customer Name")

#     # GST Details
#     gst_cgst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="CGST Amount")
#     gst_sgst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="SGST Amount")
#     gst_igst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="IGST Amount")
#     gst_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Total GST")
#     gst_cess = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="GST CESS")
#     gst_incentive = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="GST Incentive")
#     gst_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="GST Percentage")
#     gstin = models.CharField(max_length=50, blank=True, null=True, help_text="GSTIN Number")

#     # Link 1
#     link1_href = models.URLField(max_length=255, blank=True, null=True, help_text="Link 1 HREF")
#     link1_rel = models.CharField(max_length=50, blank=True, null=True, help_text="Link 1 Relation")
#     link1_method = models.CharField(max_length=10, blank=True, null=True, help_text="Link 1 HTTP Method")

#     # Link 2 (Redirect)
#     link2_href = models.URLField(max_length=255, blank=True, null=True, help_text="Link 2 HREF")
#     link2_rel = models.CharField(max_length=50, blank=True, null=True, help_text="Link 2 Relation")
#     link2_method = models.CharField(max_length=10, blank=True, null=True, help_text="Link 2 HTTP Method")

#     # Link 2 Parameters
#     link2_mercid = models.CharField(max_length=50, blank=True, null=True, help_text="Merchant ID in Link 2")
#     link2_bdorderid = models.CharField(max_length=50, blank=True, null=True, help_text="BillDesk Order ID in Link 2")
#     link2_valid_date = models.DateTimeField(blank=True, null=True, help_text="Link Valid Date")

#     # Authorization Header
#     authorization_token = models.TextField(blank=True, null=True, help_text="Authorization Token in Headers")

#     created_by = models.ForeignKey(acc_models.User, null=True, on_delete=models.SET_NULL, related_name="payment_created_by") 
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_by = models.ForeignKey(acc_models.User, null=True, on_delete=models.SET_NULL, related_name="payment_updated_by") 
#     updated_at = models.DateTimeField(auto_now = True)
    
#     def __str__(self):
#         return f"BillDesk Order {self.orderid} - {self.amount} {self.currency}"

# class BillDeskPaymentResponse(models.Model):
#     # General Transaction Details
#     objectid = models.CharField(max_length=50, help_text="Object ID (e.g., transaction)")
#     mercid = models.CharField(max_length=50, help_text="Merchant ID")
#     transaction_date = models.DateTimeField(help_text="Transaction Date and Time")
#     surcharge = models.DecimalField(max_digits=10, decimal_places=2, help_text="Surcharge Amount")
#     payment_method_type = models.CharField(max_length=50, help_text="Payment Method Type (e.g., netbanking)")
#     amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Transaction Amount")
#     ru = models.URLField(max_length=255, help_text="Return URL")
#     orderid = models.CharField(max_length=100, unique=True, help_text="Order ID")
#     transaction_error_type = models.CharField(max_length=50, help_text="Transaction Error Type")
#     discount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Discount Amount")
#     transactionid = models.CharField(max_length=100, unique=True, help_text="Transaction ID")
#     txn_process_type = models.CharField(max_length=50, help_text="Transaction Process Type")
#     bankid = models.CharField(max_length=50, help_text="Bank ID")
    
#     # Additional Information
#     additional_info1 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 1")
#     additional_info2 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 2")
#     additional_info7 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 7 (e.g., whatsapp)")

#     # Other Details
#     itemcode = models.CharField(max_length=50, help_text="Item Code")
#     transaction_error_code = models.CharField(max_length=50, help_text="Transaction Error Code")
#     currency = models.CharField(max_length=10, help_text="Currency Code")
#     auth_status = models.CharField(max_length=10, help_text="Authorization Status")
#     transaction_error_desc = models.CharField(max_length=255, help_text="Transaction Error Description")
#     charge_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total Charged Amount")
#     payment_category = models.CharField(max_length=50, help_text="Payment Category")

#     def __str__(self):
#         return f"Transaction {self.transactionid} - {self.amount} {self.currency}"


# Code for version V2.0 

# class BillDeskTransaction(models.Model):
#     # Order Details
#     mercid = models.CharField(max_length=50, help_text="Merchant ID")
#     orderid = models.CharField(max_length=50, unique=True, help_text="Order ID")
#     bdorderid = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="BillDesk Order ID")
#     amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Order Amount")
#     order_date = models.DateTimeField(help_text="Order Date and Time")
#     currency = models.CharField(max_length=10, help_text="Currency Code")
#     ru = models.URLField(max_length=255, help_text="Return URL")
#     itemcode = models.CharField(max_length=50, help_text="Item Code")
#     status = models.CharField(max_length=20, blank=True, null=True, help_text="Order Status")
#     createdon = models.DateTimeField(blank=True, null=True, help_text="Order Creation Date")
#     next_step = models.CharField(max_length=50, blank=True, null=True, help_text="Next Step (e.g., redirect)")

#     # Additional Info
#     additional_info1 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 1")
#     additional_info2 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 2")
#     additional_info7 = models.CharField(max_length=255, blank=True, null=True, help_text="Additional Info 7 (e.g., whatsapp)")

#     # Invoice Details
#     invoice_number = models.CharField(max_length=50, blank=True, null=True, help_text="Invoice Number")
#     invoice_display_number = models.CharField(max_length=50, blank=True, null=True, help_text="Invoice Display Number")
#     customer_name = models.CharField(max_length=100, blank=True, null=True, help_text="Customer Name")
#     invoice_date = models.DateTimeField(blank=True, null=True, help_text="Invoice Date")

#     # GST Details
#     gst_cgst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="CGST Amount")
#     gst_sgst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="SGST Amount")
#     gst_igst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="IGST Amount")
#     gst_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Total GST Amount")
#     gst_cess = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="GST CESS Amount")
#     gst_incentive = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="GST Incentive")
#     gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="GST Percentage")
#     gstin = models.CharField(max_length=50, blank=True, null=True, help_text="GSTIN Number")

#     # Device Details
#     device_ip = models.GenericIPAddressField(blank=True, null=True, help_text="Customer IP Address")
#     device_user_agent = models.TextField(blank=True, null=True, help_text="User Agent")

#     # Payment Response Details
#     transaction_date = models.DateTimeField(blank=True, null=True, help_text="Transaction Date and Time")
#     surcharge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Surcharge Amount")
#     payment_method_type = models.CharField(max_length=50, blank=True, null=True, help_text="Payment Method Type")
#     transactionid = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Transaction ID")
#     txn_process_type = models.CharField(max_length=50, blank=True, null=True, help_text="Transaction Process Type")
#     bankid = models.CharField(max_length=50, blank=True, null=True, help_text="Bank ID")
#     auth_status = models.CharField(max_length=10, blank=True, null=True, help_text="Authorization Status")
#     charge_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Total Charged Amount")
#     discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Discount Amount")

#     # Authorization Header
#     authorization_token = models.TextField(blank=True, null=True, help_text="Authorization Token in Headers")

#     # Timestamps
#     created_by = models.ForeignKey(acc_models.User, null=True, on_delete=models.SET_NULL, related_name="payment_created_by")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_by = models.ForeignKey(acc_models.User, null=True, on_delete=models.SET_NULL, related_name="payment_updated_by")
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Transaction {self.orderid} - {self.amount} {self.currency}"


# Respone Object
#     {
#   "objectid": "order",
#   "orderid": "ord-00039",
#   "bdorderid": "OAAN186O2CTMVEUZ",
#   "mercid": "LABOURDUAT",
#   "order_date": "2025-01-20T21:39:24+05:30",
#   "amount": "7000.00",
#   "currency": "356",
#   "ru": "https://api.diseso.com/api/application/online_payment/callback",
#   "additional_info": {
#     "additional_info1": "NA",
#     "additional_info2": "NA",
#     "additional_info3": "NA",
#     "additional_info4": "NA",
#     "additional_info5": "NA",
#     "additional_info6": "NA",
#     "additional_info7": "NA",
#     "additional_info8": "NA",
#     "additional_info9": "NA",
#     "additional_info10": "NA"
#   },
#   "itemcode": "DIRECT",
#   "createdon": "2025-01-20T21:39:24+05:30",
#   "next_step": "redirect",
#   "links": [
#     {
#       "href": "https://www.billdesk.com/pgi/ve1_2/orders/ord-00039",
#       "rel": "self",
#       "method": "GET"
#     },
#     {
#       "href": "https://uat1.billdesk.com/u2/web/v1_2/embeddedsdk",
#       "rel": "redirect",
#       "method": "POST",
#       "parameters": {
#         "mercid": "LABOURDUAT",
#         "bdorderid": "OAAN186O2CTMVEUZ",
#         "rdata": "2c391131f73ddf001a137ee3a8e454277a7fdb799d97a5cf647fba37c07fc1c68584150aefb05ea5a731d51795799f79535ca80f71637bf81dd80df6d0ca434a830b79.4145535f55415431"
#       },
#       "valid_date": "2025-01-20T22:09:24+05:30",
#       "headers": {
#         "authorization": "OToken ca001b9ead55f7f9c2042c940fc3b40449a3fea05275685c186f36c8526b799f690a831eb69c05aaa58ff1e803935b99978d1491dddedd494cf3549df9be80dcbc1881e1ee8d0680955aa61dfaca46050592ff6aa0ef8a800b85a5857426eb1cdce3208fae0690062828ae746b6693dd3fd0f8abeccab2cb913d37d67a80a04f31371a5608fb793cb969ae3ab3c897dc48ccf52a3e4c7335b12818.4145535f55415431"
#       }
#     }
#   ],
#   "status": "ACTIVE"
# }


