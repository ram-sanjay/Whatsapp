cfn_instance = ec2.CfnInstance(self, "MyCfnInstance",
    additional_info="additionalInfo",
    affinity="affinity",
    availability_zone="availabilityZone",
    block_device_mappings=[ec2.CfnInstance.BlockDeviceMappingProperty(
        device_name="deviceName",

        # the properties below are optional
        ebs=ec2.CfnInstance.EbsProperty(
            delete_on_termination=False,
            encrypted=False,
            iops=123,
            kms_key_id="kmsKeyId",
            snapshot_id="snapshotId",
            volume_size=123,
            volume_type="volumeType"
        ),
        no_device=ec2.CfnInstance.NoDeviceProperty(),
        virtual_name="virtualName"
    )],
    disable_api_termination=False,
    ebs_optimized=False,
    elastic_gpu_specifications=[ec2.CfnInstance.ElasticGpuSpecificationProperty(
        type="type"
    )],
    elastic_inference_accelerators=[ec2.CfnInstance.ElasticInferenceAcceleratorProperty(
        type="type",

        # the properties below are optional
        count=123
    )],
    enclave_options=ec2.CfnInstance.EnclaveOptionsProperty(
        enabled=False
    ),
    hibernation_options=ec2.CfnInstance.HibernationOptionsProperty(
        configured=False
    ),
    host_id="hostId",
    host_resource_group_arn="hostResourceGroupArn",
    iam_instance_profile="iamInstanceProfile",
    image_id="imageId",
    instance_initiated_shutdown_behavior="instanceInitiatedShutdownBehavior",
    instance_type="instanceType",
    ipv6_address_count=123,
    ipv6_addresses=[ec2.CfnInstance.InstanceIpv6AddressProperty(
        ipv6_address="ipv6Address"
    )],
    kernel_id="kernelId",
    key_name="keyName",
    launch_template=ec2.CfnInstance.LaunchTemplateSpecificationProperty(
        version="version",

        # the properties below are optional
        launch_template_id="launchTemplateId",
        launch_template_name="launchTemplateName"
    ),
    license_specifications=[ec2.CfnInstance.LicenseSpecificationProperty(
        license_configuration_arn="licenseConfigurationArn"
    )],
    monitoring=False,
    network_interfaces=[ec2.CfnInstance.NetworkInterfaceProperty(
        device_index="deviceIndex",

        # the properties below are optional
        associate_carrier_ip_address=False,
        associate_public_ip_address=False,
        delete_on_termination=False,
        description="description",
        group_set=["groupSet"],
        ipv6_address_count=123,
        ipv6_addresses=[ec2.CfnInstance.InstanceIpv6AddressProperty(
            ipv6_address="ipv6Address"
        )],
        network_interface_id="networkInterfaceId",
        private_ip_address="privateIpAddress",
        private_ip_addresses=[ec2.CfnInstance.PrivateIpAddressSpecificationProperty(
            primary=False,
            private_ip_address="privateIpAddress"
        )],
        secondary_private_ip_address_count=123,
        subnet_id="subnetId"
    )],

    security_group_ids=["securityGroupIds"],
    security_groups=["securityGroups"],

    subnet_id="subnetId",

)