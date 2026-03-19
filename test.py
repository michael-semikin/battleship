class VerboseAttribute:
    def __get__(self, instance, owner):
        if instance is None:
            return self  # Sınıf üzerinden erişildiğinde desktiptorun kendisini döner
        print(f"{owner.__name__} örneği üzerinden erişiliyor...")
        print(instance is self)
        return 42

class MyClass:
    x = VerboseAttribute()

obj = MyClass()
print(obj.x)  # Çıktı: MyClass örneği üzerinden erişiliyor... 42
