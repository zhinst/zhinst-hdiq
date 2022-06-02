import os
import sys


def test_source_distribution_exists(version: str, dist_dir="dist"):
    if version[0] == "v":
        version = version[1:]
    print(os.listdir(dist_dir))
    assert set(os.listdir(dist_dir)) == set([
        f"zhinst_hdiq-{version}-py3-none-any.whl",
        f"zhinst-hdiq-{version}.tar.gz"
    ])

if __name__ == "__main__":
    test_source_distribution_exists(sys.argv[1])
