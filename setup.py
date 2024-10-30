from setuptools import setup

setup(
    version="2.0.0",
    name="dcm-s11n",
    description="serialization interface for dcm",
    author="LZV.nrw",
    install_requires=[
        "dill>=0.3.7,<1.0.0",
        "dcm-common>=3.0.0,<4.0.0"
    ],
    extras_require={
        "tinydb": [
            "tinydb>=4.8.0,<5.0.0",
        ],
    },
    packages=[
        "dcm_s11n",
        "dcm_s11n.vinegar",
    ],
    package_data={"dcm_s11n": ["py.typed"]},
    setuptools_git_versioning={
        "enabled": True,
        "version_file": "VERSION",
        "count_commits_from_version_file": True,
        "dev_template": "{tag}.dev{ccount}",
    },
)
