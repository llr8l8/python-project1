from abc import ABCMeta


class Pharmacy:
    def __init__(self, name, location, is_open24_hours, opening_time=None, closing_time=None):
        self.__name = name
        self.location = location
        self.is_open24_hours = is_open24_hours
        self.opening_time = opening_time
        self.closing_time = closing_time

    @staticmethod
    def pharmacy_info():
        return "Pharmacies provide medical supplies and medication."

    def get_name(self):
        return self.__name

    def get_details(self):
        if self.is_open24_hours:
            return f"{self.__name} (24 Hours), located at {self.location}"
        return f"{self.__name}, located at {self.location}, Open: {self.opening_time} - {self.closing_time}"

    def is_available(self, current_time):
        if self.is_open24_hours:
            return True
        if self.opening_time and self.closing_time:
            opening_hour = int(self.opening_time.split()[0].split(":")[0])
            closing_hour = int(self.closing_time.split()[0].split(":")[0])
            current_hour = int(current_time.split(":")[0])
            return opening_hour <= current_hour < closing_hour
        return False


class Province(metaclass=ABCMeta):
    def __init__(self, name):
        self.__name = name
        self.pharmacies = []
        self.areas = {}

    def get_name(self):
        return self.__name

    def add_pharmacy(self, pharmacy):
        self.pharmacies.append(pharmacy)

    def get_all_pharmacies(self):
        return self.pharmacies

    def add_area(self, area):
        self.areas[area.get_name()] = area

    def get_area(self, area_name):
        return self.areas.get(area_name)


class Area(Province):
    def __init__(self, area_name, parent_province_name):
        self.area_name = area_name
        self.parent_province_name = parent_province_name
        super().__init__(parent_province_name)
        self.area_name = area_name
        self.pharmacies = []

    def get_name(self):
        return self.area_name

    def get_parent_province(self):
        return self.parent_province_name

    def add_pharmacy(self, pharmacy):
        self.pharmacies.append(pharmacy)

    def get_all_pharmacies(self):
        return self.pharmacies

    def get_available_pharmacies(self, current_time):
        return [pharmacy for pharmacy in self.pharmacies if pharmacy.is_available(current_time)]


class PharmacyDutySystem:
    def __init__(self):
        self.provinces = []

    def add_province(self, province):
        self.provinces.append(province)

    def get_province(self, province_name):
        for province in self.provinces:
            if province.get_name() == province_name:
                return province
        return None

    def search_pharmacies(self, province_name, area_name, current_time):
        province = self.get_province(province_name)
        if province:
            area = province.get_area(area_name)
            if area:
                return area.get_available_pharmacies(current_time)
        return []


if __name__ == "__main__":
    pharmacy1 = Pharmacy("الامل", "شارع بغداد", False, "8:00", "22:00")
    pharmacy2 = Pharmacy("الحياة", "شارع الزهور", True)
    pharmacy3 = Pharmacy("الصحة", "شارع الكرامة", False, "9:00", "21:00")
    pharmacy4 = Pharmacy("الشفاء", "شارع الجامعة", False, "10:00", "20:00")

    system = PharmacyDutySystem()

    province_baghdad = Province("بغداد")
    province_basra = Province("البصرة")
    area_mansour = Area("المنصور", "بغداد")
    area_zubair = Area("الزبير", "البصرة")

    area_mansour.add_pharmacy(pharmacy1)
    area_mansour.add_pharmacy(pharmacy2)
    area_zubair.add_pharmacy(pharmacy3)
    area_zubair.add_pharmacy(pharmacy4)

    province_baghdad.add_area(area_mansour)
    province_basra.add_area(area_zubair)

    system.add_province(province_baghdad)
    system.add_province(province_basra)


    def main():
        province_name = input("Enter the province  name : ")
        area_name = input(" Enter the area name: ")
        current_time = input("  Enter the current time: ")

        available_pharmacies = system.search_pharmacies(province_name, area_name, current_time)

        if available_pharmacies:
            print("Pharmacies available on time:")
            for pharmacy in available_pharmacies:
                print(pharmacy.get_details())
        else:
            print("no pharmacies available at this time:")


    main()



