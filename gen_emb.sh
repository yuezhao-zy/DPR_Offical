set -eux
export HYDRA_FULL_ERROR=1
gen_emb(){
  version=v1
#  out/nq/v1/save/

#  epoch=39


  python generate_dense_embeddings.py \
	model_file=../../$timestamp/out/$dataclass/$version/dpr_biencoder.$epoch \
	ctx_src=dpr_wiki \
	shard_id=$1 num_shards=$num_shards \
	out_file=../../$timestamp/out/$dataclass/$version/wikipedia_passages \
	batch_size=2200 #2560

}

nq_shard_0(){
    export  CUDA_VISIBLE_DEVICES=0
    gen_emb 0
}

nq_shard_1(){
    export  CUDA_VISIBLE_DEVICES=1
    gen_emb 1
}

nq_shard_2(){
    export  CUDA_VISIBLE_DEVICES=2
    gen_emb 2
}

nq_shard_3(){
    export  CUDA_VISIBLE_DEVICES=3
    gen_emb 3
}


tq_shard_0(){
    export  CUDA_VISIBLE_DEVICES=4
    gen_emb 0
}

tq_shard_1(){
    export  CUDA_VISIBLE_DEVICES=5
    gen_emb 1
}

tq_shard_2(){
    export  CUDA_VISIBLE_DEVICES=6
    gen_emb 2
}

tq_shard_3(){
    export  CUDA_VISIBLE_DEVICES=7
    gen_emb 3
}


epoch=38
if [ $1 == 'nq' ]; then

    num_shards=4
    timestamp=2022-06-22/00-29-18
    dataclass=$1
    nq_shard_0 &
    nq_shard_1 &
    nq_shard_2 &
    nq_shard_3 &

fi

webq_shard(){
    export  CUDA_VISIBLE_DEVICES=$1
    gen_emb $1
}

curatedtrec_shard(){
    export  CUDA_VISIBLE_DEVICES=$1
    gen_emb $1
}

squad_shard(){
    export  CUDA_VISIBLE_DEVICES=$1
    gen_emb $1
}


if [ $1 == 'webq' ]; then

    num_shards=8
    timestamp=2022-07-07/22-30-49
    dataclass=$1
    for i in 0 1 2 3 4 5 6 7; do
        webq_shard $i &
    done

fi

if [ $1 == 'curatedtrec' ]; then

    epoch=31
    num_shards=8
    timestamp=2022-07-08/23-28-25
    dataclass=$1
    for i in 0 1 2 3 4 5 6 7; do
        curatedtrec_shard $i &
    done

fi
if [ $1 == 'squad1' ]; then

#    epoch=37
    epoch=33
    num_shards=8
#    timestamp=2022-07-09/16-27-33
    timestamp=2022-07-11/23-18-45
    dataclass=$1
    for i in 0 1 2 3 4 5 6 7; do
        squad_shard $i &
    done

fi

tq_shard(){
    export  CUDA_VISIBLE_DEVICES=$1
    gen_emb $1

}

if [ $1 == 'trivia' ]; then

    timestamp=2022-06-22/00-27-00
    num_shards=4
    dataclass=$1
#    for i in 0 1 2 3 ; do
#        tq_shard $i &
#    done
#    tq_shard_0 &
    tq_shard_1 &
#    tq_shard_2 &
#    tq_shard_3 &


fi
