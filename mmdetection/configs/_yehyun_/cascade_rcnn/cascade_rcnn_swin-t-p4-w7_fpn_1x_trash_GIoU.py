_base_ = [
    '../_base_/models/cascade_rcnn_r50_fpn_GIoU.py',
    '../_base_/datasets/trash_detection.py',
    '../_base_/schedules/schedule_1x.py', 
    '../_base_/default_runtime.py'
]
pretrained = 'https://github.com/SwinTransformer/storage/releases/download/v1.0.0/swin_tiny_patch4_window7_224.pth'  # noqa
model = dict(
    backbone=dict(
        ## 기존의 backbone에서는 resnet50이 작성되어 있었음
        ## but, resnet50의 parameter와 swinT의 parameter 개수는 같지 않음 - depth 등등
        ## 기존에 작성된 backbone의 config를 삭제해주는 역할
        _delete_=True,

        type='SwinTransformer',
        embed_dims=96,
        depths=[2, 2, 6, 2],
        num_heads=[3, 6, 12, 24],
        window_size=7,
        mlp_ratio=4,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.,
        attn_drop_rate=0.,
        drop_path_rate=0.2,
        patch_norm=True,
        out_indices=(0, 1, 2, 3),
        with_cp=False,
        convert_weights=True,
        init_cfg=dict(type='Pretrained', checkpoint=pretrained)),
    neck=dict(in_channels=[96, 192, 384, 768]))

optimizer = dict(
    ## 기존에는 ssd optimizer였지만, adamw에 맞게 parameter 맞추기 위해 delete 진행
    _delete_=True,
    type='AdamW',
    lr=0.0001,
    betas=(0.9, 0.999),
    weight_decay=0.05,
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'relative_position_bias_table': dict(decay_mult=0.),
            'norm': dict(decay_mult=0.)
        }))
lr_config = dict(warmup_iters=1000, step=[8, 11])
runner = dict(max_epochs=12)