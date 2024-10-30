"""
Test module for the ConfigManager-class.

As of now, this only serves as a proof-of-concept for the serialization of
python objects (classes) including their references.
"""

import abc
import shutil
from pathlib import Path
import pytest
from dcm_s11n.vinegar import Vinegar, MemoryDB

WORKING_DIR = Path("tmp/")
DB_FILE = Path("test.json")

@pytest.fixture(name="example_interface", scope="session")
def get_example_interface():
    # define interface
    class FruitInterface(metaclass=abc.ABCMeta):
        @classmethod
        def __subclasshook__(cls, subclass):
            return (
                all(hasattr(subclass, x) for x in ["name", "softness", "bite"])
                    and callable(subclass.bite)
                    or NotImplemented
            )
        @property
        @abc.abstractmethod
        def name(self):
            raise NotImplementedError(
                f"Class {self.__class__.__name__} does not define property "
                "self.name"
            )
        @property
        @abc.abstractmethod
        def softness(self):
            raise NotImplementedError(
                f"Class {self.__class__.__name__} does not define property "
                "self.softness"
            )
        @abc.abstractmethod
        def bite(self) -> str:
            raise NotImplementedError(
                f"Class {self.__class__.__name__} does not define method "
                "self.bite"
            )
    return FruitInterface

@pytest.fixture(name="pickled_samples", scope="session")
def get_pickled_sample(example_interface):
    """
    Returns pickled example bytestrings generated in a separate
    environment via the script:

    import dill
    import abc

    # define interface
    class FruitInterface(metaclass=abc.ABCMeta):
        .. [see fixture above]

    # generate object
    def generate_fruit(name, softness, sound):
        class SomeFruit(FruitInterface):
            pass
        setattr(SomeFruit, "name", name)
        setattr(SomeFruit, "softness", softness)
        def bite():
            return sound
        setattr(SomeFruit, "bite", bite)

        SomeFruit.__doc__ = f"Fruit {name}"
        return SomeFruit

    # pickle
    print(dill.dumps(generate_fruit("apple", 1, "Crunch!")))
    print(dill.dumps(generate_fruit("banana", 6, "Squish!")))
    """

    return b'\x80\x04\x95"\x07\x00\x00\x00\x00\x00\x00\x8c\ndill._dill\x94\x8c\x0c_create_type\x94\x93\x94(\x8c\x03abc\x94\x8c\x07ABCMeta\x94\x93\x94\x8c\tSomeFruit\x94h\x02(h\x05\x8c\x0eFruitInterface\x94h\x00\x8c\n_load_type\x94\x93\x94\x8c\x06object\x94\x85\x94R\x94\x85\x94}\x94(\x8c\n__module__\x94\x8c\x08__main__\x94\x8c\x10__subclasshook__\x94h\t\x8c\x0bclassmethod\x94\x85\x94R\x94h\x00\x8c\x10_create_function\x94\x93\x94(h\x00\x8c\x0c_create_code\x94\x93\x94(C\n\x00\x03\x16\x01\x08\xff\x02\x02\x02\xfd\x94K\x02K\x00K\x00K\x02K\x04K\x03C$t\x00\x87\x00f\x01d\x01d\x02\x84\x08d\x03D\x00\x83\x01\x83\x01r\x10t\x01\x88\x00j\x02\x83\x01p\x11t\x03S\x00\x94(Nh\x18(C\x00\x94K\x01K\x00K\x00K\x02K\x04K3C\x1a\x81\x00|\x00]\x08}\x01t\x00\x88\x00|\x01\x83\x02V\x00\x01\x00q\x02d\x00S\x00\x94N\x85\x94\x8c\x07hasattr\x94\x85\x94\x8c\x02.0\x94\x8c\x01x\x94\x86\x94\x8c?/home/sr/working/.comitative_demonstrative/generate_testdata.py\x94\x8c\t<genexpr>\x94K\tC\x04\x02\x80\x18\x00\x94\x8c\x08subclass\x94\x85\x94)t\x94R\x94\x8c2FruitInterface.__subclasshook__.<locals>.<genexpr>\x94\x8c\x04name\x94\x8c\x08softness\x94\x8c\x04bite\x94\x87\x94t\x94(\x8c\x03all\x94\x8c\x08callable\x94h-\x8c\x0eNotImplemented\x94t\x94\x8c\x03cls\x94h&\x86\x94h#h\x11K\x06C\n\x16\x03\x08\x01\x02\xff\x02\x02\x02\xfd\x94)h\'t\x94R\x94c__builtin__\n__main__\nh\x11NNt\x94R\x94}\x94}\x94(\x8c\x0f__annotations__\x94}\x94\x8c\x0c__qualname__\x94\x8c\x1fFruitInterface.__subclasshook__\x94u\x86\x94b\x85\x94R\x94h+h\t\x8c\x08property\x94\x85\x94R\x94(h\x16(h\x18(C\x06\x00\x03\x02\x01\x0e\xff\x94K\x01K\x00K\x00K\x01K\x04KCC\x14t\x00d\x01|\x00j\x01j\x02\x9b\x00d\x02\x9d\x03\x83\x01\x82\x01\x94N\x8c\x06Class \x94\x8c# does not define property self.name\x94\x87\x94\x8c\x13NotImplementedError\x94\x8c\t__class__\x94\x8c\x08__name__\x94\x87\x94\x8c\x04self\x94\x85\x94h#h+K\rC\x06\x02\x03\x0e\x01\x04\xff\x94))t\x94R\x94c__builtin__\n__main__\nh+NNt\x94R\x94}\x94\x8c\x14__isabstractmethod__\x94\x88s}\x94(h=}\x94h?\x8c\x13FruitInterface.name\x94u\x86\x94bNNNt\x94R\x94h,hF(h\x16(h\x18(C\x06\x00\x03\x02\x01\x0e\xff\x94K\x01K\x00K\x00K\x01K\x04KChHNhI\x8c\' does not define property self.softness\x94\x87\x94hOhQh#h,K\x14hR))t\x94R\x94c__builtin__\n__main__\nh,NNt\x94R\x94}\x94hX\x88s}\x94(h=}\x94h?\x8c\x17FruitInterface.softness\x94u\x86\x94bNNNt\x94R\x94h-h\x16(h\x18(C\x06\x00\x02\x02\x01\x0e\xff\x94K\x01K\x00K\x00K\x01K\x04KChHNhI\x8c! does not define method self.bite\x94\x87\x94hOhQh#h-K\x1bC\x06\x02\x02\x0e\x01\x04\xff\x94))t\x94R\x94c__builtin__\n__main__\nh-NNt\x94R\x94}\x94hX\x88s}\x94(h=}\x94\x8c\x06return\x94h\t\x8c\x03str\x94\x85\x94R\x94sh?\x8c\x13FruitInterface.bite\x94u\x86\x94b\x8c\x07__doc__\x94N\x8c\x13__abstractmethods__\x94(h+h-h,\x91\x94ut\x94R\x94\x8c\x08builtins\x94\x8c\x07setattr\x94\x93\x94h\x82h?h\x07\x87\x94R0\x85\x94}\x94(h~\x8c\x0bFruit apple\x94h\x7f(h+h-h,\x91\x94h+\x8c\x05apple\x94h,K\x01h-h\x16(h\x18(C\x02\x00\x01\x94K\x00K\x00K\x00K\x00K\x01K\x13C\x04\x88\x00S\x00\x94h\x1d))h#h-K(C\x02\x04\x01\x94\x8c\x05sound\x94\x85\x94)t\x94R\x94c__builtin__\n__main__\nh-Nh\x00\x8c\x0c_create_cell\x94\x93\x94N\x85\x94R\x94\x85\x94t\x94R\x94}\x94}\x94(h=}\x94h?\x8c\x1cgenerate_fruit.<locals>.bite\x94u\x86\x94but\x94R\x94h\x83\x8c\x07getattr\x94\x93\x94\x8c\x04dill\x94\x8c\x05_dill\x94\x93\x94\x8c\x08_setattr\x94h\x85\x87\x94R\x94h\x96\x8c\rcell_contents\x94\x8c\x07Crunch!\x94\x87\x94R0h\x85h\xa0h?\x8c!generate_fruit.<locals>.SomeFruit\x94\x87\x94R0.', \
b"\x80\x04\x95$\x07\x00\x00\x00\x00\x00\x00\x8c\ndill._dill\x94\x8c\x0c_create_type\x94\x93\x94(\x8c\x03abc\x94\x8c\x07ABCMeta\x94\x93\x94\x8c\tSomeFruit\x94h\x02(h\x05\x8c\x0eFruitInterface\x94h\x00\x8c\n_load_type\x94\x93\x94\x8c\x06object\x94\x85\x94R\x94\x85\x94}\x94(\x8c\n__module__\x94\x8c\x08__main__\x94\x8c\x10__subclasshook__\x94h\t\x8c\x0bclassmethod\x94\x85\x94R\x94h\x00\x8c\x10_create_function\x94\x93\x94(h\x00\x8c\x0c_create_code\x94\x93\x94(C\n\x00\x03\x16\x01\x08\xff\x02\x02\x02\xfd\x94K\x02K\x00K\x00K\x02K\x04K\x03C$t\x00\x87\x00f\x01d\x01d\x02\x84\x08d\x03D\x00\x83\x01\x83\x01r\x10t\x01\x88\x00j\x02\x83\x01p\x11t\x03S\x00\x94(Nh\x18(C\x00\x94K\x01K\x00K\x00K\x02K\x04K3C\x1a\x81\x00|\x00]\x08}\x01t\x00\x88\x00|\x01\x83\x02V\x00\x01\x00q\x02d\x00S\x00\x94N\x85\x94\x8c\x07hasattr\x94\x85\x94\x8c\x02.0\x94\x8c\x01x\x94\x86\x94\x8c?/home/sr/working/.comitative_demonstrative/generate_testdata.py\x94\x8c\t<genexpr>\x94K\tC\x04\x02\x80\x18\x00\x94\x8c\x08subclass\x94\x85\x94)t\x94R\x94\x8c2FruitInterface.__subclasshook__.<locals>.<genexpr>\x94\x8c\x04name\x94\x8c\x08softness\x94\x8c\x04bite\x94\x87\x94t\x94(\x8c\x03all\x94\x8c\x08callable\x94h-\x8c\x0eNotImplemented\x94t\x94\x8c\x03cls\x94h&\x86\x94h#h\x11K\x06C\n\x16\x03\x08\x01\x02\xff\x02\x02\x02\xfd\x94)h't\x94R\x94c__builtin__\n__main__\nh\x11NNt\x94R\x94}\x94}\x94(\x8c\x0f__annotations__\x94}\x94\x8c\x0c__qualname__\x94\x8c\x1fFruitInterface.__subclasshook__\x94u\x86\x94b\x85\x94R\x94h+h\t\x8c\x08property\x94\x85\x94R\x94(h\x16(h\x18(C\x06\x00\x03\x02\x01\x0e\xff\x94K\x01K\x00K\x00K\x01K\x04KCC\x14t\x00d\x01|\x00j\x01j\x02\x9b\x00d\x02\x9d\x03\x83\x01\x82\x01\x94N\x8c\x06Class \x94\x8c# does not define property self.name\x94\x87\x94\x8c\x13NotImplementedError\x94\x8c\t__class__\x94\x8c\x08__name__\x94\x87\x94\x8c\x04self\x94\x85\x94h#h+K\rC\x06\x02\x03\x0e\x01\x04\xff\x94))t\x94R\x94c__builtin__\n__main__\nh+NNt\x94R\x94}\x94\x8c\x14__isabstractmethod__\x94\x88s}\x94(h=}\x94h?\x8c\x13FruitInterface.name\x94u\x86\x94bNNNt\x94R\x94h,hF(h\x16(h\x18(C\x06\x00\x03\x02\x01\x0e\xff\x94K\x01K\x00K\x00K\x01K\x04KChHNhI\x8c' does not define property self.softness\x94\x87\x94hOhQh#h,K\x14hR))t\x94R\x94c__builtin__\n__main__\nh,NNt\x94R\x94}\x94hX\x88s}\x94(h=}\x94h?\x8c\x17FruitInterface.softness\x94u\x86\x94bNNNt\x94R\x94h-h\x16(h\x18(C\x06\x00\x02\x02\x01\x0e\xff\x94K\x01K\x00K\x00K\x01K\x04KChHNhI\x8c! does not define method self.bite\x94\x87\x94hOhQh#h-K\x1bC\x06\x02\x02\x0e\x01\x04\xff\x94))t\x94R\x94c__builtin__\n__main__\nh-NNt\x94R\x94}\x94hX\x88s}\x94(h=}\x94\x8c\x06return\x94h\t\x8c\x03str\x94\x85\x94R\x94sh?\x8c\x13FruitInterface.bite\x94u\x86\x94b\x8c\x07__doc__\x94N\x8c\x13__abstractmethods__\x94(h+h-h,\x91\x94ut\x94R\x94\x8c\x08builtins\x94\x8c\x07setattr\x94\x93\x94h\x82h?h\x07\x87\x94R0\x85\x94}\x94(h~\x8c\x0cFruit banana\x94h\x7f(h+h-h,\x91\x94h+\x8c\x06banana\x94h,K\x06h-h\x16(h\x18(C\x02\x00\x01\x94K\x00K\x00K\x00K\x00K\x01K\x13C\x04\x88\x00S\x00\x94h\x1d))h#h-K(C\x02\x04\x01\x94\x8c\x05sound\x94\x85\x94)t\x94R\x94c__builtin__\n__main__\nh-Nh\x00\x8c\x0c_create_cell\x94\x93\x94N\x85\x94R\x94\x85\x94t\x94R\x94}\x94}\x94(h=}\x94h?\x8c\x1cgenerate_fruit.<locals>.bite\x94u\x86\x94but\x94R\x94h\x83\x8c\x07getattr\x94\x93\x94\x8c\x04dill\x94\x8c\x05_dill\x94\x93\x94\x8c\x08_setattr\x94h\x85\x87\x94R\x94h\x96\x8c\rcell_contents\x94\x8c\x07Squish!\x94\x87\x94R0h\x85h\xa0h?\x8c!generate_fruit.<locals>.SomeFruit\x94\x87\x94R0."

@pytest.fixture(scope="session", autouse=True)
def prepare_session(request):
    """
    Cleanup working dir pre- and post-test.

    Prepare serialized class-objects from local scope.
    """
    def cleanup():
        if WORKING_DIR.is_dir():
            shutil.rmtree(WORKING_DIR)

    # prepare working dir for SerializationManager
    cleanup()
    WORKING_DIR.mkdir(parents=True, exist_ok=True)

    request.addfinalizer(cleanup)

@pytest.fixture(name="simple_class", scope="session")
def make_simple_class():
    """
    Simple class for (de-)serialization.
    """
    class Jar():
        volume = 1
        lid = True
        def open(self):
            self.lid = False

    return Jar

@pytest.fixture(name="plain_vinegar")
def make_plain_vinegar():
    # cleanup Vinegar
    if (WORKING_DIR / DB_FILE).is_file():
        (WORKING_DIR / DB_FILE).unlink()
    # generate new Vinegar
    plain_db = MemoryDB()
    plain_vinegar = Vinegar(plain_db)

    return plain_vinegar

def test_dill_applicability(plain_vinegar, example_interface, pickled_samples):
    """
    Test Vinegar.loads for pre-generated bytestrings of objects.

    See doc of fixture pickled_samples above.
    """

    # deserialize apple
    apple_restored = plain_vinegar.loads(pickled_samples[0])

    assert apple_restored.name == "apple"
    assert apple_restored.softness == 1
    assert apple_restored.bite() == "Crunch!"
    assert issubclass(apple_restored, example_interface)

    # deserialize banana
    banana_restored = plain_vinegar.loads(pickled_samples[1])

    assert banana_restored.name == "banana"
    assert banana_restored.softness == 6
    assert banana_restored.bite() == "Squish!"
    assert issubclass(banana_restored, example_interface)

def test_vinegar_instantiation():
    """Test instantiation of Vinegar-objects."""

    # cleanup Vinegar
    if (WORKING_DIR / DB_FILE).is_file():
        (WORKING_DIR / DB_FILE).unlink()

    some_db = MemoryDB()
    some_vinegar = Vinegar(some_db)
    assert some_vinegar.find() == []

def test_dump_and_load_record(plain_vinegar, simple_class):
    """Test adding records to Vinegar-object db."""

    plain_vinegar.dump(simple_class, tag="test")

    everything = plain_vinegar.find()

    assert len(everything) == 1

    restored_jar_class = plain_vinegar.load(tag="test")
    restored_jar = restored_jar_class()

    assert restored_jar.volume == 1
    assert restored_jar.lid
    restored_jar.open()
    assert not restored_jar.lid

def test_find_record(plain_vinegar):
    """Test list of record in vinegar-database."""

    class Apple():
        name = "apple"
    class Banana():
        name = "banana"

    # add two records to db
    plain_vinegar.dump(Apple, tag=Apple.name)
    plain_vinegar.dump(Banana, tag=Banana.name)
    test2 = plain_vinegar.find(Banana.name)
    assert test2 == {"tag": Banana.name, "obj": plain_vinegar.dumps(Banana)}

def test_remove_record(plain_vinegar, simple_class):
    """Test removal of record in vinegar-database."""

    # add two records to db
    plain_vinegar.dump(simple_class, tag="test")
    plain_vinegar.dump(simple_class, tag="test2")
    everything = plain_vinegar.find()
    assert len(everything) == 2

    # remove this record again
    plain_vinegar.remove("test")
    everything = plain_vinegar.find()
    assert len(everything) == 1
