"""
Pairplot Library - セットアップスクリプト
"""
from setuptools import setup, find_packages
import os

# README.mdの内容を読み込む
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# requirements.txtから依存関係を読み込む
def read_requirements():
    """requirements.txtから依存関係のリストを読み込む"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="pairplot-lib",
    version="1.0.1",
    author="Takayuki Tsuji",
    description="CSVデータからペアプロット、散布図、箱ひげ図を生成するツール（白黒描画）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takasan1234/pairplot-lib",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "pairplot=pairplot_lib.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

