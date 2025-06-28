"""
Shared pytest fixtures and configuration for all tests.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pandas as pd
import numpy as np


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_config():
    """Provide a mock configuration object."""
    config = Mock()
    config.debug = False
    config.log_level = "INFO"
    config.data_dir = "/tmp/test_data"
    return config


@pytest.fixture
def sample_dataframe():
    """Create a sample pandas DataFrame for testing."""
    dates = pd.date_range(start='2023-01-01', end='2023-01-10', freq='D')
    data = {
        'Open': np.random.uniform(100, 110, len(dates)),
        'High': np.random.uniform(110, 120, len(dates)),
        'Low': np.random.uniform(90, 100, len(dates)),
        'Close': np.random.uniform(95, 115, len(dates)),
        'Volume': np.random.randint(1000000, 5000000, len(dates))
    }
    df = pd.DataFrame(data, index=dates)
    return df


@pytest.fixture
def mock_market_data():
    """Mock market data provider."""
    mock = MagicMock()
    mock.get_historical_data.return_value = pd.DataFrame({
        'Close': [100, 101, 99, 102, 103],
        'Volume': [1000000, 1100000, 900000, 1200000, 1050000]
    })
    return mock


@pytest.fixture
def mock_order():
    """Create a mock order object."""
    order = Mock()
    order.symbol = "AAPL"
    order.quantity = 100
    order.price = 150.0
    order.side = "BUY"
    order.order_type = "LIMIT"
    order.status = "PENDING"
    return order


@pytest.fixture
def mock_portfolio():
    """Create a mock portfolio object."""
    portfolio = Mock()
    portfolio.cash = 100000.0
    portfolio.positions = {}
    portfolio.get_total_value = Mock(return_value=100000.0)
    portfolio.get_position = Mock(return_value=0)
    return portfolio


@pytest.fixture(autouse=True)
def reset_random_seed():
    """Reset random seeds for reproducible tests."""
    np.random.seed(42)
    import random
    random.seed(42)


@pytest.fixture
def captured_logs(caplog):
    """Fixture to capture log messages."""
    with caplog.at_level("DEBUG"):
        yield caplog


@pytest.fixture
def mock_file_system(mocker):
    """Mock file system operations."""
    mock_open = mocker.mock_open(read_data="test data")
    mocker.patch("builtins.open", mock_open)
    return mock_open


@pytest.fixture
def clean_imports(monkeypatch):
    """Clean module imports between tests."""
    import sys
    modules_backup = sys.modules.copy()
    yield
    # Restore original modules
    sys.modules.clear()
    sys.modules.update(modules_backup)