from typing import Any, Optional
from rest_framework import Response


class ApiResponse:

    @staticmethod
    def success(
        data: Any = None, message: str = "Success", status_code: int = 200
    ) -> Response:

        return Response(
            {"Success": True, "message": message, "data": data, "error": None},
            status=status_code,
        )

    @staticmethod
    def error(
        message: str,
        error_code: Optional[str] = None,
        status_code: int = 400,
        details: Any = None,
    ) -> Response:
        return Response(
            {
                "success": False,
                "message": message,
                "data": None,
                "error": {"code": error_code, "details": details},
            }
        )
