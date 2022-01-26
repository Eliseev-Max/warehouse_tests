import time
import allure
import pytest


@allure.title("Проверка качества сигнала выбранного канала")
@allure.description("Проверяем, является ли хорошим качество сигнала")
def test_quality_of_signal(ssh_connection, channel_indicator):
    wh_view = ssh_connection.send_command(channel_indicator.warehouse_view()).get_result()
    assert channel_indicator.handle_warehouse_view(wh_view)["QUAL"] == channel_indicator.GOOD_QUAL_SIGN


@allure.title("Проверка изменения значения канала")
@allure.description("Проверяем, изменится ли значение выбранного канала после принудительной установки значения "
                    "командой \"warehouse_set\"")
@pytest.mark.parametrize("channel_val", [1, 0])
def test_change_channel_value(ssh_connection, channel_indicator, channel_val):
    ssh_connection.send_command(channel_indicator.warehouse_set(channel_val))
    time.sleep(0.5)
    data_output = ssh_connection.send_command(channel_indicator.warehouse_view()).get_result()
    assert channel_indicator.handle_warehouse_view(data_output)["VALUE"] == channel_val


@allure.title("Проверка изменения качества сигнала")
@allure.description("Проверяем, изменится ли качество сигнала после принудительной установки значения "
                    "качества командой \"warehouse_set\"")
@pytest.mark.parametrize("quality", ["-", "+"])
def test_change_quality_of_signal(ssh_connection, channel_indicator, quality):
    QUAL = channel_indicator.BAD
    if quality == "+":
        QUAL = channel_indicator.GOOD
    ssh_connection.send_command(channel_indicator.warehouse_set(0, quality=QUAL))
    time.sleep(0.2)
    data_output = ssh_connection.send_command(channel_indicator.warehouse_view()).get_result()
    assert channel_indicator.handle_warehouse_view(data_output)["QUAL"] == quality
