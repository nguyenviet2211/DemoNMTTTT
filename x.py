# import pandas as pd

# # Đọc file CSV
# try:
#     df = pd.read_csv('train_sms_vi.csv')
# except FileNotFoundError:
#     print(f"Lỗi: Không tìm thấy file train_sms_vi.csv")
#     exit()

# # Tìm các hàng bị trùng lặp (giữ lại tất cả các bản sao của hàng trùng lặp)
# duplicate_rows = df[df.duplicated(keep=False)]

# # Kiểm tra xem có hàng nào bị trùng lặp không
# if duplicate_rows.empty:
#     print("Không tìm thấy hàng nào bị trùng lặp trong file train_sms_vi.csv")
# else:
#     print("Các hàng sau đây bị trùng lặp trong file train_sms_vi.csv:")
#     print(duplicate_rows.to_string())





# Xóa những dòng trùng
import pandas as pd

# Đường dẫn đến file CSV
file_path = 'train_sms_vi.csv'

try:
    # Đọc file CSV
    df = pd.read_csv(file_path)

    # Lưu lại số lượng hàng trước khi xóa
    rows_before = len(df)

    # Xóa các hàng trùng lặp, giữ lại hàng đầu tiên
    df.drop_duplicates(keep='first', inplace=True)

    # Lưu lại số lượng hàng sau khi xóa
    rows_after = len(df)

    # Ghi lại DataFrame đã được làm sạch vào file CSV
    df.to_csv(file_path, index=False, encoding='utf-8')

    print(f"Đã đọc file: {file_path}")
    print(f"Số hàng trước khi xóa: {rows_before}")
    print(f"Số hàng sau khi xóa: {rows_after}")
    print(f"Số hàng đã xóa: {rows_before - rows_after}")
    print(f"Đã xóa các hàng trùng lặp và lưu lại vào file {file_path}")

except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file {file_path}")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
