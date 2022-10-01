
train_part() {
    version=v1/
    dataclass=$1
    #      python train_dense_encoder.py \
    python -m torch.distributed.launch --master_port $master_port \
        --nproc_per_node=$nproc_per_node train_dense_encoder.py \
        train_datasets=[${dataclass}_train_part] \
        dev_datasets=[${dataclass}_dev_local] \
        train=biencoder_local \
        output_dir=out/$dataclass/$version
}


dense_retrieve() {
#    epoch=38
    model_path=../../../outputs/$timestamp/out/$dataclass/$version
    python dense_retriever.py \
        model_file=$model_path/dpr_biencoder.${epoch} \
        qa_dataset=${dataclass}_${cp} \
        ctx_datatsets=[dpr_wiki] \
        encoded_ctx_files=[\"$model_path/wikipedia_passages_*\"] \
        batch_size=256 \
        out_file=$model_path/${cp}_pred.json
    #	encoded_ctx_files=[\"~/myproject/embeddings_passages1/wiki_passages_*\",\"~/myproject/embeddings_passages2/wiki_passages_*\"] \
}


#epoch=38
epoch=31
#train
if [ $1 == 'nq_train' ]; then
    export  CUDA_VISIBLE_DEVICES=2,3,4
    nproc_per_node=3
    master_port=43227
#    pretrained_model_cfg=bert-base-uncased
    pretrained_model_cfg=Luyu/co-condenser-wiki
    train_part nq
fi

if [ $1 == 'trivia_train' ]; then
    export  CUDA_VISIBLE_DEVICES=5,6,7
    nproc_per_node=3
    master_port=43225
#    pretrained_model_cfg=bert-base-uncased
    pretrained_model_cfg=Luyu/co-condenser-wiki
    train_part trivia
fi

if [ $1 == 'webq_train' ]; then
    export  CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
    nproc_per_node=8
    master_port=43225
#    pretrained_model_cfg=bert-base-uncased
#    pretrained_model_cfg=Luyu/co-condenser-wiki
    train_part webq
fi

if [ $1 == 'squad1_train' ]; then
    export  CUDA_VISIBLE_DEVICES=0,1,2,3
    nproc_per_node=4
    master_port=43225
#    pretrained_model_cfg=bert-base-uncased
#    pretrained_model_cfg=Luyu/co-condenser-wiki
    train_part squad1
fi

if [ $1 == 'curatedtrec_train' ]; then
    export  CUDA_VISIBLE_DEVICES=0,1,2,3
    nproc_per_node=4
    master_port=43225
#    pretrained_model_cfg=bert-base-uncased
#    pretrained_model_cfg=Luyu/co-condenser-wiki
    train_part curatedtrec
fi

if [ $1 == 'nq' ]; then
    timestamp=2022-06-22/00-29-18
    dataclass=$1
    version=v1
    export CUDA_VISIBLE_DEVICES=1
#    for cp in test dev  train  ; do
    for cp in   train  ; do
        dense_retrieve
    done
fi

if [ $1 == 'trivia' ]; then
    timestamp=2022-06-22/00-27-00
    dataclass=$1
    version=v1
    export CUDA_VISIBLE_DEVICES=2
    for cp in test dev  train  ; do
        dense_retrieve
    done
fi


if [ $1 == 'webq' ]; then
#    timestamp=2022-07-05/14-20-16
    timestamp=2022-07-07/22-30-49
    dataclass=$1
    version=v1
    export CUDA_VISIBLE_DEVICES=1
    for cp in test dev train  ; do
        dense_retrieve
    done
fi


if [ $1 == 'curatedtrec' ]; then
    timestamp=2022-07-08/23-28-25
    dataclass=$1
    version=v1
    export CUDA_VISIBLE_DEVICES=1
    for cp in test dev train  ; do
        dense_retrieve
    done
fi


if [ $1 == 'squad1' ]; then
#    epoch=37
    epoch=33
#    timestamp=2022-07-09/16-27-33
    timestamp=2022-07-11/23-18-45
    dataclass=$1
    version=v1
    export CUDA_VISIBLE_DEVICES=1
    for cp in test dev train  ; do
        dense_retrieve
    done
fi

