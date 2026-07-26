class Validator:

    def __init__(self):

        self.passed = 0
        self.failed = 0

    def success(self, message):

        self.passed += 1
        print(f"✔ {message}")

    def failure(self, message):

        self.failed += 1
        print(f"✘ {message}")

    def section(self, title):

        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)

    def summary(self):

        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        print(f"Passed : {self.passed}")
        print(f"Failed : {self.failed}")

        if self.failed == 0:
            print("\n🎉 Dataset validation PASSED")
        else:
            print("\n❌ Dataset validation FAILED")