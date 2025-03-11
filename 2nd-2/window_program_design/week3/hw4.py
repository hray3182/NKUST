def read_file():
    file = open("zip.csv", "r", encoding="utf-8")
    for line in file:
        city, area, zipcode = line.strip().split(",")
        if city not in data:
            data[city] = {}
        if area not in data[city]:
            data[city][area] = zipcode
    file.close()


def list_zip(city):
    if city not in data:
        return None
    return data[city]    

def area_to_zip(area):
    result = {}
    for city in data:
        if area in data[city]:
            result[city] = data[city][area]
    return result if result else None

def zip_to_area(zip):
    for city in data:
        for area in data[city]:
            if data[city][area] == zip:
                return area
    return None

if __name__ == "__main__":
    data = {}
    read_file()
    while True:
        print("1. 列出該縣市的所有行政區")
        print("2. 列出該行政區的郵遞區號")
        print("3. 列出該郵遞區號的行政區")
        print("4. 離開")
        choice = input("請輸入選項: ")
        if choice == "1":
            city = input("請輸入縣市: ").replace("台", "臺")
            city_data = list_zip(city)
            if city_data is None:
                print("找不到該縣市")
                continue
            for area in city_data:
                print(area)
        elif choice == "2":
            area = input("請輸入行政區: ")
            result = area_to_zip(area)
            if result is None:
                print("找不到該行政區")
                continue
            for city, zipcode in result.items():
                print(f"{city} {area}: {zipcode}")
        elif choice == "3":
            zip = input("請輸入郵遞區號: ")
            print(zip_to_area(zip))
        elif choice == "4":
            break
        else:
            print("請輸入有效的選項")


