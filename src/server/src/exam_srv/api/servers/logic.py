"""Business logic for /widgets API endpoints."""
from http import HTTPStatus

from flask import jsonify, url_for
from flask_restx import abort, marshal

from exam_srv import db
from exam_srv.api.auth.decorators import token_required, admin_token_required
from exam_srv.api.servers.dto import pagination_model, server_name
from exam_srv.models.user import User
from exam_srv.models.server import Server


@token_required
def create_server(server_dict):
    name = server_dict["name"]
    if Server.find_by_name(name):
        error = f"Server name: {name} already exists, must be unique."
        abort(HTTPStatus.CONFLICT, error, status="fail")
    server = Server(**server_dict)
    owner = User.find_by_public_id(create_server.public_id)
    server.owner_id = owner.id
    db.session.add(server)
    db.session.commit()
    response = jsonify(status="success", message=f"New server added: {name}.")
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for("api.server", name=name)
    return response


@token_required
def retrieve_server_list(page, per_page):
    owner = User.find_by_public_id(retrieve_server_list.public_id)
    pagination = Server.query.filter(Server.owner_id == owner.id).paginate(page=page, per_page=per_page,
                                                                           error_out=False)
    response_data = marshal(pagination, pagination_model)
    response_data["links"] = _pagination_nav_links(pagination)
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination)
    response.headers["Total-Count"] = pagination.total
    return response


# @token_required
def retrieve_server(name):
    return Server.query.filter_by(name=name).first_or_404(  # .lower()
        description=f"{name} not found in database."
    )


@admin_token_required
def update_server(name, server_dict):
    server = Server.find_by_name(name)  #.lower()
    if server:
        for k, v in server_dict.items():
            setattr(server, k, v)
        db.session.commit()
        message = f"'{name}' was successfully updated"
        response_dict = dict(status="success", message=message)
        return response_dict, HTTPStatus.OK
    try:
        valid_name = server_name(name)  #.lower()
    except ValueError as e:
        abort(HTTPStatus.BAD_REQUEST, str(e), status="fail")
    server_dict["name"] = valid_name
    return create_server(server_dict)


@token_required
def delete_server(name):
    server = Server.query.filter_by(name=name).first_or_404(  #.lower()
        description=f"{name} not found in database."
    )
    db.session.delete(server)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT


def _pagination_nav_links(pagination):
    nav_links = {}
    per_page = pagination.per_page
    this_page = pagination.page
    last_page = pagination.pages
    nav_links["self"] = url_for("api.server_list", page=this_page, per_page=per_page)
    nav_links["first"] = url_for("api.server_list", page=1, per_page=per_page)
    if pagination.has_prev:
        nav_links["prev"] = url_for(
            "api.server_list", page=this_page - 1, per_page=per_page
        )
    if pagination.has_next:
        nav_links["next"] = url_for(
            "api.server_list", page=this_page + 1, per_page=per_page
        )
    nav_links["last"] = url_for("api.server_list", page=last_page, per_page=per_page)
    return nav_links


def _pagination_nav_header_links(pagination):
    url_dict = _pagination_nav_links(pagination)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f'<{url}>; rel="{rel}", '
    return link_header.strip().strip(",")
