from django.shortcuts import redirect
from django.views import generic
from django.views.generic import TemplateView

from .forms import PurchaseTorBridgeOnHostForm
from .models import Host, ShopPurchaseOrder
from django.shortcuts import render
from shop.models import Host


class HostListView(generic.ListView):
    model = Host

    def get_queryset(self):
        return Host.active.all()


class PurchaseTorBridgeOnHostView(generic.UpdateView):
    model = Host
    form_class = PurchaseTorBridgeOnHostForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # print(context)
        return context

    def get_queryset(self):
        return Host.active.all()

    def get_success_url(self):
        pass

    def form_valid(self, form):
        clean_target = form.cleaned_data.get('target')
        clean_comment = form.cleaned_data.get('comment')

        # tor_bridge = TorBridge.objects.create(comment=clean_comment,
        #                                       host=form.instance,
        #                                       target=clean_target)
        #
        # po = PurchaseOrder.objects.create()
        # po_item = PurchaseOrderItemDetail(price=form.instance.tor_bridge_price_initial,
        #                                   product=tor_bridge,
        #                                   quantity=1)
        # po.item_details.add(po_item, bulk=False)
        # po_item.save()
        # po.save()
        
        host=form.instance
        if not host.tor_bridge_ports_available(consider_safety_margin=True):
            raise Exception('The current host does not have any Tor bridge ports available.')
        po = ShopPurchaseOrder.tor_bridges.create(host=host, target=clean_target, comment=clean_comment)

        return redirect('lnpurchase:po-detail', pk=po.pk)
        # return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print("form invalid")  # ToDo(frennkie) use messages
        return super().form_invalid(form)


class DemoView(TemplateView):
    template_name = 'shop/demo.html'


def index(request):
    return  render(request, 'shop/landing.html', { 'object_list': Host.active.all()})