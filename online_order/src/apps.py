from django.apps import AppConfig


class SrcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src'



# @session_required_admin
# def agent_all_pending_transaction_payment(request, tp=None, ag=None):
#     if tp and ag:
#         try:
#             trans = request.GET.getlist('trans')
#             trans = json.loads(trans)
#             amt = request.GET.get('amt')
#             amt = json.loads(amt)
#
#             transactions = AgentTransactions.objects.filter(id__in=trans).order_by('id')
#             agent = DeliveryAgent.objects.get(id=ag)
#             return_dict = {
#                 'transactions': transactions,
#                 'amt': amt,
#                 'ag': ag,
#                 'tp': tp,
#                 'trans': trans,
#                 'agent': agent,
#             }
#             if tp == 'credit':
#                 if request.method == 'POST':
#                     try:
#                         payment_obj = AgentPayment()
#                         payment_obj.delivery_agent = agent
#                         payment_obj.reference_id = request.POST.get('reference_id')
#                         payment_obj.pay_by = request.POST.get('pay_by')
#                         payment_obj.is_credit = True
#                         payment_obj.is_paid = True
#                         payment_obj.amount = amt
#                         payment_obj.save()
#                         for i in transactions:
#                             i.is_completed = True
#                             i.save()
#                             payment_obj.transactions.add(i)
#
#                         messages.add_message(request, messages.SUCCESS, 'All pending transactions are processed')
#                         return redirect('agent_payment_home')
#                     except Exception as e:
#                         messages.add_message(request, messages.WARNING, e)
#                     return redirect('agent_all_pending_transaction_payment', tp=tp, ag=ag)
#                 return render(request, 'sys_admin/agent_all_pending_transaction_payment.html', return_dict)
#             elif tp == 'debit':
#                 if request.method == 'POST':
#                     try:
#                         payment_obj = AgentPayment()
#                         payment_obj.delivery_agent = agent
#                         payment_obj.reference_id = request.POST.get('reference_id')
#                         payment_obj.pay_by = request.POST.get('pay_by')
#                         payment_obj.is_debit = True
#                         payment_obj.is_paid = True
#                         payment_obj.amount = amt
#                         payment_obj.save()
#                         for i in transactions:
#                             i.is_completed = True
#                             i.save()
#                             payment_obj.transactions.add(i)
#
#                         messages.add_message(request, messages.SUCCESS, 'All pending transactions are processed')
#                         return redirect('agent_payment_home')
#                     except Exception as e:
#                         messages.add_message(request, messages.WARNING, e)
#                     return redirect('agent_all_pending_transaction_payment', tp=tp, ag=ag)
#                 return render(request, 'sys_admin/agent_all_pending_transaction_payment.html', return_dict)
#         except Exception as e:
#             messages.add_message(request, messages.WARNING, e)
#             return redirect('agent_payment_home')
#     else:
#         messages.add_message(request, messages.WARNING, 'Payment Type is needed to proceed payment request!')
#         return redirect('agent_payment_home')



# function debit_payment_request(trans, amount, agent_id){
#        var conf = confirm('Are you sure about this transaction? amount'+amount+'/- will be debited from Admin Account');
#        if(conf){
#             console.log(trans, amount, agent_id);
#             if(trans && amount && agent_id){
#                 $.ajax({
#                     type: 'GET',
#                     dataType : 'JSON',
#                     url:  '/agent_all_pending_transaction_payment/debit/'+agent_id+'/',
#                     async:  false,
#                     data:{
#                          'trans[]': JSON.stringify(trans),
#                          'amt': JSON.stringify(amount),
#                     },
#                     success:function(data){
#                         console.log(data);
#                     }
#                 });
#             }
#        }
#     }
#     function credit_payment_request(trans, amount, agent_id){
#         var conf = confirm("Are you sure about this transaction? amount"+amount+"/- will be credited to Admin Account");
#         if(conf){
#             console.log(trans, amount, agent_id);
#             if(trans && amount && agent_id){
#                 $.ajax({
#                     type: 'GET',
#                     dataType : 'JSON',
#                     url:  '/agent_all_pending_transaction_payment/credit/'+agent_id+'/',
#                     async:  false,
#                     data:{
#                          'trans[]': JSON.stringify(trans),
#                          'amt': JSON.stringify(amount),
#                     },
#                     success:function(data){
#                        console.log(data);
#                     }
#                 });
#             }
#         }
#     }