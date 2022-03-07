"""
Flows for br_cvm_administradores_carteira
"""

from prefect import Flow
from prefect.run_configs import KubernetesRun
from prefect.storage import GCS
from pipelines.constants import constants
from pipelines.datasets.br_cvm_administradores_carteira.tasks import (
    crawl,
    clean_table_responsavel,
    clean_table_pessoa_fisica,
    clean_table_pessoa_juridica,
)
from pipelines.constants import constants
from pipelines.tasks import upload_to_gcs, create_bd_table, dump_header_to_csv
from pipelines.datasets.br_cvm_administradores_carteira.schedules import every_day

ROOT = "/tmp/basedosdados"
URL = "http://dados.cvm.gov.br/dados/ADM_CART/CAD/DADOS/cad_adm_cart.zip"

with Flow("br_cvm_administradores_carteira.responsavel") as br_cvm_adm_car_res:
    crawl(ROOT, URL)
    filepath = clean_table_responsavel(ROOT)
    dataset_id = "br_cvm_administradores_carteira"
    table_id = "responsavel"

    wait_header_path = dump_header_to_csv(data_path=filepath)

    # Create table in BigQuery
    wait_create_bd_table = create_bd_table(  # pylint: disable=invalid-name
        path=wait_header_path,
        dataset_id=dataset_id,
        table_id=table_id,
        dump_type="overwrite",
        wait=wait_header_path,
    )

    # Upload to GCS
    upload_to_gcs(
        path=filepath,
        dataset_id=dataset_id,
        table_id=table_id,
        wait=wait_create_bd_table,
    )

br_cvm_adm_car_res.storage = GCS(constants.GCS_FLOWS_BUCKET.value)
br_cvm_adm_car_res.run_config = KubernetesRun(image=constants.DOCKER_IMAGE.value)
br_cvm_adm_car_res.schedule = every_day

with Flow("br_cvm_administradores_carteira.pessoa_fisica") as br_cvm_adm_car_pes_fis:
    crawl(ROOT, URL)
    filepath = clean_table_pessoa_fisica(ROOT)
    dataset_id = "br_cvm_administradores_carteira"
    table_id = "pessoa_fisica"

    wait_header_path = dump_header_to_csv(data_path=filepath)

    # Create table in BigQuery
    wait_create_bd_table = create_bd_table(  # pylint: disable=invalid-name
        path=wait_header_path,
        dataset_id=dataset_id,
        table_id=table_id,
        dump_type="overwrite",
        wait=wait_header_path,
    )

    # Upload to GCS
    upload_to_gcs(
        path=filepath,
        dataset_id=dataset_id,
        table_id=table_id,
        wait=wait_create_bd_table,
    )

br_cvm_adm_car_pes_fis.storage = GCS(constants.GCS_FLOWS_BUCKET.value)
br_cvm_adm_car_pes_fis.run_config = KubernetesRun(image=constants.DOCKER_IMAGE.value)
br_cvm_adm_car_pes_fis.schedule = every_day

with Flow("br_cvm_administradores_carteira.pessoa_juridica") as br_cvm_adm_car_pes_jur:
    crawl(ROOT, URL)
    filepath = clean_table_pessoa_juridica(ROOT)
    dataset_id = "br_cvm_administradores_carteira"
    table_id = "pessoa_juridica"

    wait_header_path = dump_header_to_csv(data_path=filepath)

    # Create table in BigQuery
    wait_create_bd_table = create_bd_table(  # pylint: disable=invalid-name
        path=wait_header_path,
        dataset_id=dataset_id,
        table_id=table_id,
        dump_type="overwrite",
        wait=wait_header_path,
    )

    # Upload to GCS
    upload_to_gcs(
        path=filepath,
        dataset_id=dataset_id,
        table_id=table_id,
        wait=wait_create_bd_table,
    )

br_cvm_adm_car_pes_jur.storage = GCS(constants.GCS_FLOWS_BUCKET.value)
br_cvm_adm_car_pes_jur.run_config = KubernetesRun(image=constants.DOCKER_IMAGE.value)
br_cvm_adm_car_pes_jur.schedule = every_day
