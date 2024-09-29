"""API endpoint definitions for /servers namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource

from exam_srv.api.servers.dto import (
    create_server_reqparser,
    update_server_reqparser,
    pagination_reqparser,
    server_owner_model,
    server_model,
    pagination_links_model,
    pagination_model,
)
from exam_srv.api.servers.logic import (
    create_server,
    retrieve_server_list,
    retrieve_server,
    update_server,
    delete_server,
)

server_ns = Namespace(name="servers", validate=True)
server_ns.models[server_owner_model.name] = server_owner_model
server_ns.models[server_model.name] = server_model
server_ns.models[pagination_links_model.name] = pagination_links_model
server_ns.models[pagination_model.name] = pagination_model


@server_ns.route("", endpoint="server_list")
@server_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@server_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@server_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class ServerList(Resource):
    """Handles HTTP requests to URL: /servers."""

    @server_ns.doc(security="Bearer")
    @server_ns.response(int(HTTPStatus.OK), "Retrieved server list.", pagination_model)
    @server_ns.expect(pagination_reqparser)
    def get(self):
        """Retrieve a list of servers."""
        request_data = pagination_reqparser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_server_list(page, per_page)

    @server_ns.doc(security="Bearer")
    @server_ns.response(int(HTTPStatus.CREATED), "Added new server.")
    @server_ns.response(int(HTTPStatus.FORBIDDEN), "Token required.")
    @server_ns.response(int(HTTPStatus.CONFLICT), "Server name already exists.")
    @server_ns.expect(create_server_reqparser)
    def post(self):
        """Create a server."""
        server_dict = create_server_reqparser.parse_args()
        return create_server(server_dict)


@server_ns.route("/<name>", endpoint="server")
@server_ns.param("name", "Server name")
@server_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@server_ns.response(int(HTTPStatus.NOT_FOUND), "Server not found.")
@server_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@server_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Server(Resource):
    """Handles HTTP requests to URL: /servers/{name}."""

    @server_ns.doc(security="Bearer")
    @server_ns.response(int(HTTPStatus.OK), "Retrieved server.", server_model)
    @server_ns.marshal_with(server_model)
    def get(self, name):
        """Retrieve a server."""
        return retrieve_server(name)

    @server_ns.doc(security="Bearer")
    @server_ns.response(int(HTTPStatus.OK), "Server was updated.", server_model)
    @server_ns.response(int(HTTPStatus.CREATED), "Added new server.")
    @server_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @server_ns.expect(update_server_reqparser)
    def put(self, name):
        """Update a server."""
        server_dict = update_server_reqparser.parse_args()
        return update_server(name, server_dict)

    @server_ns.doc(security="Bearer")
    @server_ns.response(int(HTTPStatus.NO_CONTENT), "Server was deleted.")
    @server_ns.response(int(HTTPStatus.FORBIDDEN), "Token required.")
    def delete(self, name):
        """Delete a widget."""
        return delete_server(name)
