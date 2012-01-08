from mysite.invoice.models import Invoice, Item
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.admin.views.decorators import staff_member_required
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis

def get_total(year, month):
    if month is None:
        invoices = Invoice.objects.filter(date__year)
    else:
        invoices = Invoice.objects.filter(date__year=year, date__month=month)
    total = 0
    for invoice in invoices:
        total += invoice.total
        
    return total

def report(request):
    # data report
    if Invoice.objects.all().count() == 0:
        return redirect("/openbook")
    min_year = Invoice.objects.order_by("date")[0].date.year
    max_year = Invoice.objects.order_by("-date")[0].date.year
    report = []
    for year in range(min_year,max_year+1):
        year_report = []
        for month in range(1,13):
            total = get_total(year, month)
            year_report.append(total)
        s = sum(year_report)
        tax = round((s * (0.13 / 1.13)), 2)
        year_report.append(tax)
        year_report.append(s)
        year_report.insert(0, year)
        report.append(year_report)
        
    # graphical data year report
    year_total_data = [i[-1] for i in report]
    max_y = max(year_total_data)
    min_y = min(year_total_data)
    gr = SimpleLineChart(800, 300, y_range=[0,max_y])
    gr.add_data(year_total_data)
    gr.set_grid(0, 25, 5, 5)
    left_axis = range(min_y, max_y + 1, (max_y/10))
    left_axis[0] = ''
    gr.set_axis_labels(Axis.LEFT, left_axis)
    gr.set_axis_labels(Axis.BOTTOM, \
    [str(i) for i in range(min_year, max_year+1)])
    
    # yearly report
    gs = []
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    for data in report:
        max_y = max(data[1:-2]) # excluding the first and the last 2 entries
        g = SimpleLineChart(800, 300, y_range=[0, max_y])
        g.add_data(data[1:-2]) # excluding the frist and the last 2 entries
        g.set_grid(0, 25, 5, 5)
        left_axis = range(0, max_y + 1, (max_y/10))
        left_axis[0] = ''
        g.set_axis_labels(Axis.LEFT, left_axis)
        g.set_axis_labels(Axis.BOTTOM, \
        months)
        gs.append((data[0], g.get_url()))
    gs.reverse()
    grurl = gr.get_url()
    if max_year == min_year:
        grurl = None
    return render_to_response(
        "admin/invoice/report.html",
        {'report' : report, 'gr': grurl, 'gs':gs},
        RequestContext(request, {}),
    )
report = staff_member_required(report)
