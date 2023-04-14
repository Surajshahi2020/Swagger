from rest_framework import generics, status
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from accounts.api.serializers.accounts import MemberSerializer, MemberUpdateSerializer
from common.pagination import CustomPagination
from common.serializer import OperationError, OperationSuccess
from rest_framework.response import Response
from rest_framework import viewsets
from accounts.models import Member


@extend_schema_view(
    post=extend_schema(
        description="User Create Api",
        summary="Refer To Schemas At Bottom",
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
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
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
    serializer_class = MemberSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    delete=extend_schema(
        description="My User Delete Api",
        summary="Uer Deleted Details",
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
    serializer_class = MemberUpdateSerializer

    http_method_names = [
        "patch",
    ]

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
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
