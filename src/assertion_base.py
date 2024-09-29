import logging
from logs.custom_errors import CodeLogMsg

logger = logging.getLogger("LOGGER_ASSERTIONS")


class BaseAssertion:
    @staticmethod
    def assert_status_code(response, expected_code):
        assert response.status_code == expected_code, CodeLogMsg(response) \
            .add_compare_result(response.status_code, expected_code) \
            .add_request_info() \
            .add_response_info() \
            .get_message()


