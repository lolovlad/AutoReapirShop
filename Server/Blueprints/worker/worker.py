from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from Server.Service import OrderService, AutoService
from Server.Forms import SearchOrderWorkerForm, OrderAddForm

from Server.Models import state_order, type_order
from Server.database import db


worker_router = Blueprint("worker", __name__, template_folder="templates", static_folder="static")


menu = [
    {"url": "worker_blueprint.order", "title": "Заказы"},
]


@worker_router.before_request
def is_worker():
    if current_user.is_authenticated:
        user_role = current_user.user.role.name
        if "worker" != user_role:
            return redirect("/")
    else:
        return redirect("/")


@worker_router.route("/", methods=["GET"])
@login_required
def index():
    return redirect(url_for('.order'))


@worker_router.route("/orders", methods=["GET", "POST"])
@login_required
def order():

    args = request.args
    form = SearchOrderWorkerForm()

    state_order = args.get("state_order")
    service = OrderService(db.session)

    state_orders = [(i.id, f"{i.name}") for i in service.get_state_order()]

    form.state_order.choices = state_orders

    if state_order is None:
        state_order = state_orders[0][0]

    if request.method == "GET":
        orders_entity = service.get_order_by_auto_mechanic_id_and_state_order(current_user.user.id, state_order)
        return render_template("order_worker.html",
                               menu=menu,
                               user=current_user,
                               list_order=orders_entity,
                               form=form)
    elif request.method == "POST":
        return redirect(url_for("worker_blueprint.order", state_order=form.state_order.data))


@worker_router.route("/order/<uuid>", methods=["GET"])
@login_required
def order_info(uuid: str):

    service = OrderService(db.session)
    orders_entity = service.get_by_trace_id(uuid)

    return render_template("info_order_worker.html",
                           menu=menu,
                           user=current_user,
                           order=orders_entity)


@worker_router.route("/order/update/<uuid>", methods=["GET", "POST"])
@login_required
def update_order(uuid: str):
    form = OrderAddForm()
    service_order = OrderService(db.session)

    order = service_order.get_by_trace_id(uuid)

    service_auto = AutoService(db.session)
    form.auto.choices = [(i.id, f"{i.brand} {i.model}") for i in service_auto.get_list_auto_by_id(order.client_id)]
    form.auto_mechanic.choices = [(i.id, f"{i}") for i in service_order.get_auto_mechanic()]

    form.state_order.choices = [(i.id, f"{i.name}") for i in service_order.get_state_order()]
    form.auto_mechanic.data = order.auto_mechanic_id

    if request.method == "GET":

        form.auto.data = order.auto_id
        form.state_order.data = order.state_order_id

        form.description.data = order.description

        return render_template("order_update_worker.html", current_user=current_user, menu=menu, form=form, order=order)

    elif request.method == "POST":
        if form.validate_on_submit():
            service_order.update(
                uuid,
                form.auto_mechanic.data,
                form.auto.data,
                form.state_order.data,
                form.description.data,
            )
            return redirect(url_for('.order_info', uuid=uuid))
        else:
            print(uuid, form.auto_mechanic.data, form.auto.data, form.state_order.data, form.description.data)
            return redirect(url_for('.update_order', uuid=uuid))

