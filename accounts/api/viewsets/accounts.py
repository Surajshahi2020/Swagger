from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from accounts.api.serializers.accounts import (
    MemberSerializer,
    MemberUpdateSerializer,
    LoginSerializer,
)
from common.pagination import CustomPagination
from common.serializer import OperationError, OperationSuccess
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from common.exceptions import UnprocessableEntityException


from rest_framework.response import Response
from rest_framework import viewsets
from accounts.models import Member
import datetime
import json
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


@extend_schema_view(
    post=extend_schema(
        description="Creating user details",
        summary="User create ",
        request=MemberSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when User is created successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["User Api"],
    ),
)
class UserCreateView(generics.CreateAPIView):
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if "email" not in data:
            return Response(
                {"title": "User create", "message": "Email is required"},
                status=422,
            )
        if Member.objects.filter(email=data["email"]).exists():
            return Response(
                {
                    "title": "User Create",
                    "message": "User with this Email already exists !",
                },
                status=422,
            )
        serializer = self.get_serializer(None, request.data)
        serializer.is_valid(raise_exception=True)
        dat = serializer.create(serializer.validated_data)
        dat = self.get_serializer(dat).data
        return Response(
            {
                "title": "User Create",
                "message": "User Created Successfully!",
                "data": dat,
            }
        )


@extend_schema_view(
    get=extend_schema(
        description="My User List Api",
        summary="List User Details",
        # request=UserSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when user is retrived successfully!",
            ),
            401: OpenApiResponse(
                response=OperationError,
                description="Fetched error!",
            ),
        },
        tags=["User Api"],
    ),
)
class UserListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            resp = self.get_paginated_response(serializer.data)
            return Response(
                {
                    "title": "User List",
                    "message": "List fetched successfully",
                    "data": resp.data,
                }
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "title": "User List",
                "message": "List fetched successfully",
                "data": serializer.data,
            }
        )


@extend_schema_view(
    get=extend_schema(
        description="My User Fetching Api",
        summary="Fetch User Details",
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when user is retrived successfully!",
            ),
            401: OpenApiResponse(
                response=OperationError,
                description="Fetched error!",
            ),
        },
        tags=["User Api"],
    ),
)
class UserDetailView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    delete=extend_schema(
        description="My User Delete Api",
        summary="User Deleted Details",
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when user is deleted successfully!",
            ),
            401: OpenApiResponse(
                response=OperationError,
                description="Fetched error!",
            ),
        },
        tags=["User Api"],
    ),
)
class UserDeleteView(generics.DestroyAPIView):
    queryset = Member.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "title": "User Delete",
                "message": "User deleted successfully",
            }
        )

    def perform_destroy(self, instance):
        instance.delete()


@extend_schema_view(
    patch=extend_schema(
        description="User Update Api",
        summary="Refer To Schemas At Bottom",
        request=MemberUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when user is updated successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["User Api"],
    ),
)
class UserUpdateView(generics.UpdateAPIView):
    queryset = Member.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MemberUpdateSerializer

    http_method_names = [
        "patch",
    ]

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        data = request.data

        if "email" in data:
            if data["email"] != "":
                if (
                    Member.objects.filter(email=data["email"]).first()
                    != self.request.user
                    and data["email"]
                ):
                    return Response(
                        {
                            "title": "User Update",
                            "message": "Email already linked with another user!",
                        },
                        status=422,
                    )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        updated_data = self.get_serializer(instance).data
        return Response(
            {
                "title": "User Updated",
                "message": "User Updated Successfully!",
                "data": updated_data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        description="User Login Api",
        summary="Email Login Api",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when user is loggedin successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Login Apis"],
    ),
)
class EmailLoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = Member.objects.filter(email=data.get("email"))
        if user.exists():
            user: Member = user.first()
            if user.is_blocked:
                return Response(
                    {
                        "title": "Login",
                        "message": "Account Blocked !",
                    },
                    status=401,
                )
            if user.check_password(data.get("password")):
                refresh = RefreshToken.for_user(user)
                refresh.set_exp(lifetime=datetime.timedelta(days=14))
                access = refresh.access_token
                access.set_exp(lifetime=datetime.timedelta(days=1))
                return Response(
                    {
                        "title": "Login",
                        "message": "Logged in successfully !",
                        "data": {
                            **MemberSerializer(user, many=False).data,
                            "access": f"{access}",
                            "refresh": f"{refresh}",
                        },
                    },
                    status=200,
                )
            else:
                return Response(
                    {
                        "title": "Login",
                        "message": "Password incorrect !",
                    },
                    status=422,
                )
        else:
            return Response(
                {
                    "title": "Login",
                    "message": "Email does not exist!",
                },
                status=422,
            )


@extend_schema_view(
    post=extend_schema(
        description="User Refresh Api",
        summary="Refresh Token Api",
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when token refreshed successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Login Apis"],
    ),
)
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise UnprocessableEntityException(
                {
                    "title": "Login Refresh",
                    "message": e.args[0],
                },
                code=422,
            )

        return Response(
            {
                "title": "Login Refresh",
                "message": "Login Refreshed Successfully!",
                "data": serializer.validated_data,
            },
            status=200,
        )
