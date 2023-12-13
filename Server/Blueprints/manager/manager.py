from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required

from Server.Service import ClientService, AutoService, OrderService

from Server.database import db

from Server.Forms import ClientForm, AutoForm, OrderAddForm, OrderServiceUpdateForm

manager_router = Blueprint("manager", __name__, template_folder="templates", static_folder="static")


menu = [
    {"url": "manager_blueprint.client", "title": "Клиенты"},
    {"url": "manager_blueprint.order", "title": "Заказы"},
]


@manager_router.before_request
def is_manager():
    if current_user.is_authenticated:
        user_role = current_user.user.role.name
        if "manager" != user_role:
            return redirect("/")
    else:
        return redirect("/")


@manager_router.route("/", methods=["GET"])
@login_required
def index():
    return redirect(url_for('.client'))


@manager_router.route("/client", methods=["GET"])
@login_required
def client():
    service = ClientService(db.session)
    list_client = service.get_list_client()
    return render_template("client.html", current_user=current_user, menu=menu, clients=list_client)


@manager_router.route("/client/add", methods=["GET", "POST"])
@login_required
def add_client():
    form = ClientForm()
    if request.method == "GET":
        return render_template("client_form.html", current_user=current_user, menu=menu, form=form,
                               action=url_for("manager_blueprint.add_client"))

    elif request.method == "POST":
        if form.validate_on_submit():
            service = ClientService(db.session)
            service.add(form.name.data,
                        form.surname.data,
                        form.patronymics.data,
                        form.phone.data,
                        form.email.data)

            return redirect(url_for('.client'))
        else:
            return redirect(url_for('.add_client'))


@manager_router.route("/client/delete/<uuid>", methods=["GET"])
@login_required
def delete_client(uuid: str):
    service = ClientService(db.session)

    service.delete(uuid)

    return redirect(url_for('.client'))


@manager_router.route("/client/update/<uuid>", methods=["GET", "POST"])
@login_required
def update_client(uuid: str):
    form = ClientForm()
    service = ClientService(db.session)

    if request.method == "GET":

        client_entity = service.get_by_trace_id(uuid)
        form.name.data = client_entity.name
        form.surname.data = client_entity.surname
        form.patronymics.data = client_entity.patronymics
        form.phone.data = client_entity.phone
        form.email.data = client_entity.email

        return render_template("client_form.html", current_user=current_user, menu=menu, form=form,
                               action=url_for("manager_blueprint.update_client", uuid=client_entity.trace_id))

    elif request.method == "POST":
        if form.validate_on_submit():
            service.update(uuid,
                           form.name.data,
                           form.surname.data,
                           form.patronymics.data,
                           form.phone.data,
                           form.email.data)

            return redirect(url_for('.client'))
        else:
            return redirect(url_for('.update_client'))

########################################################################################################################


@manager_router.route("/client/<uuid>/auto", methods=["GET"])
@login_required
def auto(uuid: str):
    service = AutoService(db.session)
    list_auto = service.get_list_auto(uuid)
    return render_template("auto.html", current_user=current_user, menu=menu, list_auto=list_auto, client_uuid=uuid)


@manager_router.route("/client/<uuid>/auto/add", methods=["GET", "POST"])
@login_required
def add_auto(uuid: str):
    form = AutoForm()
    if request.method == "GET":
        return render_template("auto_form.html", current_user=current_user, menu=menu, form=form,
                               action=url_for("manager_blueprint.add_auto", uuid=uuid))

    elif request.method == "POST":
        if form.validate_on_submit():
            service = AutoService(db.session)
            service.add(uuid,
                        form.model.data,
                        form.brand.data,
                        form.number.data,
                        form.region.data,
                        form.vin_number.data)

            return redirect(url_for('.auto', uuid=uuid))
        else:
            return redirect(url_for('.add_auto', uuid=uuid))


@manager_router.route("/client/<uuid>/auto/update/<uuid_auto>", methods=["GET", "POST"])
@login_required
def update_auto(uuid: str, uuid_auto: str):
    form = AutoForm()
    service = AutoService(db.session)

    if request.method == "GET":

        client_entity = service.get_by_trace_id(uuid_auto)
        form.model.data = client_entity.model
        form.brand.data = client_entity.brand
        form.number.data = client_entity.number
        form.region.data = client_entity.region
        form.vin_number.data = client_entity.vin_number

        return render_template("auto_form.html", current_user=current_user, menu=menu, form=form,
                               action=url_for("manager_blueprint.update_auto",
                                              uuid=uuid,
                                              uuid_auto=client_entity.trace_id))

    elif request.method == "POST":
        if form.validate_on_submit():
            service.update(uuid_auto,
                           form.model.data,
                           form.brand.data,
                           form.number.data,
                           form.region.data,
                           form.vin_number.data)

            return redirect(url_for('.auto', uuid=uuid))
        else:
            return redirect(url_for('.update_auto', uuid=uuid, uuid_auto=uuid_auto))


@manager_router.route("/client/<uuid>/auto/delete/<uuid_auto>", methods=["GET"])
@login_required
def delete_auto(uuid: str, uuid_auto: str):
    service = AutoService(db.session)

    service.delete(uuid_auto)

    return redirect(url_for('.auto', uuid=uuid))


#######################################################################################################################

@manager_router.route("/order", methods=["GET", "POST"])
@login_required
def order():
    service = OrderService(db.session)

    list_order = service.get_list_order()

    return render_template("order.html", current_user=current_user, menu=menu, list_order=list_order)


@manager_router.route("/order/add/<uuid>", methods=["GET", "POST"])
@login_required
def add_order(uuid: str):
    form = OrderAddForm()
    service_order = OrderService(db.session)

    service_auto = AutoService(db.session)
    form.auto.choices = [(i.id, f"{i.brand} {i.model}") for i in service_auto.get_list_auto_by_trace(uuid)]
    form.auto_mechanic.choices = [(i.id, f"{i}") for i in service_order.get_auto_mechanic()]

    form.state_order.choices = [(i.id, f"{i.name}") for i in service_order.get_state_order()]

    form.services.choices = [(i.id, f"{i.name}") for i in service_order.get_list_service()]
    if request.method == "GET":
        return render_template("order_add.html", current_user=current_user, menu=menu, form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            service_order.add(
                uuid,
                form.auto_mechanic.data,
                form.auto.data,
                form.state_order.data,
                form.description.data,
                form.services.data
            )
            return redirect(url_for('.client', uuid=uuid))
        else:
            return redirect(url_for('.add_order', uuid=uuid))


@manager_router.route("/order/details/<uuid>", methods=["GET"])
@login_required
def details_order(uuid: str):
    service = OrderService(db.session)
    order = service.get_by_trace_id(uuid)
    return render_template("details_order.html", current_user=current_user, menu=menu, order=order)


@manager_router.route("/order/delete/<int:id_order>", methods=["GET"])
@login_required
def delete_order():
    pass


@manager_router.route("/order/update/<uuid>", methods=["GET", "POST"])
@login_required
def update_order(uuid: str):
    form = OrderAddForm()
    service_order = OrderService(db.session)

    order = service_order.get_by_trace_id(uuid)

    service_auto = AutoService(db.session)
    form.auto.choices = [(i.id, f"{i.brand} {i.model}") for i in service_auto.get_list_auto_by_id(order.client_id)]
    form.auto_mechanic.choices = [(i.id, f"{i}") for i in service_order.get_auto_mechanic()]

    form.state_order.choices = [(i.id, f"{i.name}") for i in service_order.get_state_order()]

    if request.method == "GET":

        form.auto.data = order.auto_id
        form.auto_mechanic.data = order.auto_mechanic_id
        form.state_order.data = order.state_order_id

        form.description.data = order.description

        return render_template("order_update.html", current_user=current_user, menu=menu, form=form, order=order)

    elif request.method == "POST":
        if form.validate_on_submit():
            service_order.update(
                uuid,
                form.auto_mechanic.data,
                form.auto.data,
                form.state_order.data,
                form.description.data,
            )
            return redirect(url_for('.details_order', uuid=uuid))
        else:
            return redirect(url_for('.update_order', uuid=uuid))


@manager_router.route("/order/service/<int:id_order>/<int:id_service>", methods=["GET", "POST"])
@login_required
def update_service_order(id_order: int, id_service: int):

    form = OrderServiceUpdateForm()
    service = OrderService(db.session)
    order_service = service.get_order_service(id_order, id_service)

    if request.method == "GET":
        form.count.data = order_service.count
        return render_template("order_service_update.html", current_user=current_user, menu=menu, service=order_service,
                               form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            service.update_order_service(id_order, id_service, form.count.data)
            return redirect(url_for('.back_order', id_order=id_order))


@manager_router.route("/order/service/back/<int:id_order>", methods=["GET", "POST"])
@login_required
def back_order(id_order: int):
    service = OrderService(db.session)
    entity = service.get(id_order)
    return redirect(url_for('.details_order', uuid=entity.trace_id))

