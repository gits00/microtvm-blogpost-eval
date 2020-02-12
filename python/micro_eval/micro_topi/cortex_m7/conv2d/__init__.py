def gen_conv2d(data_layout, kernel_layout):
    assert data_layout == "NHWC"
    assert kernel_layout == "HWOI"
    mod = relay.fromtext(f"""
    v0.0.4
    def @main(
        %data: Tensor[(1, 16, 16, 32), int8],
        %kernel: Tensor[(5, 5, 32, 32), int8]) {{
      %0 = nn.conv2d(
        %data,
        %kernel,
        padding=[2, 2],
        channels=32,
        kernel_size=[5, 5],
        data_layout="NHWC",
        kernel_layout="HWOI",
        out_dtype="int32");
      %1 = right_shift(%0, 9);
      cast(%1, "int8")
    }}
    """)

    # generate random params
    params = {}
    for param in mod['main'].params[1:]:
        shape = list(map(lambda x: x.value, param.checked_type.shape))
        dtype = param.checked_type.dtype
        if 'kernel' in param.name_hint:
            result = tvm.nd.array(np.random.randint(-30, 30, size=shape, dtype=dtype), tvm.cpu(0))
        else:
            assert False
        params[param.name_hint] = result

    return mod, params
