from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from src.config.config import conf
from src.utils.logging import logger


def get_assets(asset_class: AssetClass):

    logger.info("+++++++++++++++ ASSETS +++++++++++++++")
    trading_client = TradingClient(
        api_key=conf.alpaca_creds.api_key,
        secret_key=conf.alpaca_creds.secret_key.get_secret_value(),
    )

    # search for crypto assets
    search_params = GetAssetsRequest(asset_class=asset_class)

    assets = trading_client.get_all_assets(search_params)
    assets_names = [x.name for x in assets]

    logger.info(f"Assets: {assets_names}")

    logger.info("--------------- ASSETS ---------------")


if __name__ == "__main__":
    get_assets(asset_class=AssetClass.CRYPTO)
