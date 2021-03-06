# __author__ = 'Vasudev Gupta'
from dataclasses import dataclass, replace, field
import torch

from torch_trainer import DefaultArgs
from transformers.models.bart.adapter_modeling import AdapterConfig
from transformers import MBartConfig


@dataclass
class TrainerConfig(DefaultArgs):

    tgt_file: str = 'data/parallel/IITB.en-hi.en'
    src_file: str = 'data/parallel/IITB.en-hi.hi'
    single_file: bool = False

    src_lang: str = 'hi_IN'
    max_length: int = 40
    max_target_length: int = 40

    tr_max_samples: int = -1
    val_max_samples: int = -1
    finetuned_id: str = "dummy"

    save_specific: bool = False
    load_specific_path: str = None # "specific-layers"

    batch_size: int = 32
    lr: float = 1e-3

    model_id: str = "facebook/mbart-large-cc25" # "vasudevgupta/mbart-iitb-hin-eng"
    tokenizer_id: str = "facebook/mbart-large-cc25"

    base_dir: str = "base_dir"
    tb_grads: str = "tb_grads"
    tb_params: str = "tb_params"

    test_size: float = .03
    random_seed:  int = 7232114
    num_workers: int = 2
    max_pred_length: int = 40

    tgt_lang: str = 'en_XX'

    # control adapter from here
    # manually switch off layers in case you want to freeze
    load_adapter_path: str = None
    save_adapter_path: str = None
    enc_ffn_adapter: bool = False
    dec_ffn_adapter: bool = False
    enc_self_attn_adapter: bool = False
    dec_self_attn_adapter: bool = False
    cross_attn_adapter: bool = False
    enc_tok_embed_adapter: bool = False
    dec_tok_embed_adapter: bool = False

    # trainable-status of some parts of network
    embed_grad: bool = True
    pos_embed_grad: bool = True
    enc_ffn_grad: bool = True
    dec_ffn_grad: bool = True
    enc_attn_grad: bool = True
    dec_attn_grad: bool = True
    cross_attn_grad: bool = True
    enc_norm_grad: bool = True
    dec_norm_grad: bool = True
    cross_attn_norm_grad: bool = True

    # args used in torch_trainer
    max_epochs: int = 5
    accumulation_steps: int = 1
    save_epoch_dir: str = None
    early_stop_n: int = None
    map_location: torch.device = torch.device("cuda:0")
    save_dir: str = None
    load_dir: str = None
    tpus: int = 0
    precision: str = 'float32'
    fast_dev_run: bool = False

    # all these args will be invalid if you run sweep
    project_name: str = 'transformers-adapters'
    wandb_run_name: str = None
    wandb_off: bool = False
    wandb_resume: bool = False
    wandb_run_id: str = None

    # bart inside config
    bart_config: MBartConfig = field(repr=False, default=MBartConfig.from_pretrained(model_id))

    # adapter inside config
    enc_ffn_adapter_config: AdapterConfig = field(repr=False, default=AdapterConfig(input_size=1024))

    dec_ffn_adapter_config: AdapterConfig = field(repr=False, default=AdapterConfig(input_size=1024))

    enc_self_attn_adapter_config: AdapterConfig = field(repr=False, default=AdapterConfig(input_size=1024))

    dec_self_attn_adapter_config: AdapterConfig = field(repr=False, default=AdapterConfig(input_size=1024))

    cross_attn_adapter_config: AdapterConfig = field(repr=False, default=AdapterConfig(input_size=1024))

    dec_tok_embed_adapter_config: AdapterConfig = field(repr=False, default=AdapterConfig(input_size=1024,
                                                                                        add_layer_norm_after=False))

    enc_tok_embed_adapter_config: AdapterConfig = field(repr=False, default=AdapterConfig(input_size=1024,
                                                                                        add_layer_norm_after=False))


iitb_hin = TrainerConfig(tgt_file='parallel/IITB.en-hi.en', 
                    src_file='parallel/IITB.en-hi.hi',
                    src_lang="hi_IN",
                    max_length=32,
                    max_target_length=32,
                    base_dir="iitb_base_dir")

bhasha_hin = TrainerConfig(tgt_file="pib-v1.3/en-hi/train.en", 
                    src_file="pib-v1.3/en-hi/train.hi",
                    src_lang="hi_IN",
                    max_length=40,
                    max_target_length=40,
                    test_size=0.03)

bhasha_guj = TrainerConfig(tgt_file="pib-v1.3/en-gu/train.en", 
                    src_file="pib-v1.3/en-gu/train.gu",
                    src_lang="gu_IN",
                    max_length=40,
                    max_target_length=40,
                    base_dir="guj_base_dir",
                    test_size=0.13)

config_adapt_sa_ffn = replace(bhasha_hin,
                        enc_ffn_adapter=True,
                        dec_ffn_adapter=True,
                        enc_self_attn_adapter=True,
                        dec_self_attn_adapter=True,
                        embed_grad=False,
                        pos_embed_grad=False,
                        enc_ffn_grad=False,
                        dec_ffn_grad=False,
                        enc_attn_grad=False,
                        dec_attn_grad=False,
                        cross_attn_grad=False,
                        enc_norm_grad=False,
                        dec_norm_grad=False,
                        cross_attn_norm_grad=False,
                        base_dir="config_adapt_sa_ffn",
                        save_adapter_path=None)

freeze_model_hin = replace(bhasha_hin,
                    base_dir="tr_dec-ffn_enc-attn_embed_hin2000,400",
                    wandb_run_name="tr_dec-ffn_enc-attn_embed_hin2000,400",
                    embed_grad=False,
                    pos_embed_grad=False,
                    enc_ffn_grad=False,
                    dec_ffn_grad=False,
                    enc_attn_grad=False,
                    dec_attn_grad=False,
                    cross_attn_grad=False,
                    enc_norm_grad=False,
                    dec_norm_grad=False,
                    cross_attn_norm_grad=False,
                    save_specific=False,
                    # load_specific_path="specific-layers.pt",
                    max_length=40,
                    max_target_length=40)

freeze_model_guj = replace(bhasha_guj,
                    base_dir="tr_dec-ffn_enc-attn_embed_hin2000,400",
                    wandb_run_name="tr_dec-ffn_enc-attn_embed_hin2000,400",
                    embed_grad=False,
                    pos_embed_grad=False,
                    enc_ffn_grad=False,
                    dec_ffn_grad=False,
                    enc_attn_grad=False,
                    dec_attn_grad=False,
                    cross_attn_grad=False,
                    enc_norm_grad=False,
                    dec_norm_grad=False,
                    cross_attn_norm_grad=False,
                    save_specific=False,
                    # load_specific_path="specific-layers.pt",
                    max_length=40,
                    max_target_length=40)


best_adapters_hin = replace(freeze_model_hin,
            enc_self_attn_adapter=True,
            dec_ffn_adapter=True,
            enc_tok_embed_adapter=True,
            dec_tok_embed_adapter=True,
            save_adapter_path="adapter",
            # load_adapter_path="adapter.pt",
            base_dir="final-best-adapters-hindi",
            wandb_run_name="final-best-adapters-hin",
            finetuned_id="offnote-mbart-adapters-hin-eng",
            lr=1e-3,
            max_epochs=5)

best_adapters_guj = replace(freeze_model_guj,
            enc_self_attn_adapter=True,
            dec_ffn_adapter=True,
            enc_tok_embed_adapter=True,
            dec_tok_embed_adapter=True,
            save_adapter_path="adapter",
            # load_adapter_path="adapter.pt",
            base_dir="final-best-adapters-guj",
            wandb_run_name="final-best-adapters-guj",
            finetuned_id="offnote-mbart-adapters-guj-eng",
            lr=1e-3,
            max_epochs=5)

full_train_guj = replace(bhasha_guj,
            base_dir="mbart-bhasha-guj-eng",
            wandb_run_name="mbart-bhasha-guj-eng",
            finetuned_id="mbart-bhasha-guj-eng",
            lr=5e-5,
            max_epochs=3)

full_train_hin = replace(bhasha_hin,
            base_dir="mbart-bhasha-hin-eng",
            wandb_run_name="mbart-bhasha-hin-eng",
            finetuned_id="mbart-bhasha-hin-eng",
            lr=5e-5,
            max_epochs=3)

# this is getting called in `main.py`
# main = full_train_hin
# if sweep is defined then these args will work like default
# and will be overwritten by wandb
