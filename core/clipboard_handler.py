"""
Module xử lý clipboard cho text, rich text và ảnh
"""
import pyperclip
import win32clipboard
import win32con
from PIL import Image
import io
import os
import time
import pyautogui

class ClipboardHandler:
    @staticmethod
    def copy_text(text: str):
        """Copy văn bản thuần vào clipboard với tốc độ tối ưu"""
        try:
            # Kiểm tra độ dài và warn nếu quá lớn
            if len(text) > 100000:
                print(f"Cảnh báo: Văn bản rất dài ({len(text)} ký tự), đang copy...")
            
            # Sử dụng pyperclip trước vì nó nhanh hơn và ít conflict
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    pyperclip.copy(text)
                    print(f"Đã copy thành công {len(text)} ký tự (pyperclip)")
                    return True
                except Exception as e1:
                    if attempt < max_retries - 1:
                        time.sleep(0.001)  # Micro delay rồi thử lại
                        continue
                    
                    # Fallback sang win32clipboard với retry
                    print(f"pyperclip thất bại, thử win32clipboard: {e1}")
                    
                    for win_attempt in range(2):
                        try:
                            win32clipboard.OpenClipboard()
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardText(text)
                            win32clipboard.CloseClipboard()
                            print(f"Đã copy thành công với win32clipboard: {len(text)} ký tự")
                            return True
                        except Exception as e2:
                            try:
                                win32clipboard.CloseClipboard()
                            except:
                                pass
                            if win_attempt == 0:
                                time.sleep(0.002)  # 2ms delay rồi thử lại
                                continue
                            else:
                                print(f"Lỗi cuối cùng: {e2}")
                                return False
            
            return False
            
        except Exception as e:
            print(f"Lỗi không mong đợi: {e}")
            return False
    
    @staticmethod
    def copy_html(html_text: str):
        """Copy văn bản (text thuần hoặc HTML) vào clipboard với tốc độ tối ưu"""
        try:
            # Kiểm tra độ dài văn bản - với văn bản rất dài, dùng copy_text trực tiếp
            if len(html_text) > 50000:  # Giảm threshold để ưu tiên tốc độ
                print(f"Văn bản dài ({len(html_text)} ký tự), dùng copy_text để tăng tốc")
                return ClipboardHandler.copy_text(html_text)
            
            # Kiểm tra xem có phải HTML không
            is_html = '<' in html_text and '>' in html_text
            
            if not is_html:
                # Text thuần - escape nhanh
                html_content = (html_text
                    .replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                    .replace('\n', '<br>'))
            else:
                html_content = html_text
            
            # Template đơn giản hóa để tăng tốc
            html_template = """Version:0.9
StartHTML:000000071
EndHTML:{end_html:09d}
StartFragment:000000140
EndFragment:{end_fragment:09d}
<html><head><meta charset="utf-8"></head><body><!--StartFragment-->{html_content}<!--EndFragment--></body></html>"""
            
            # Tính toán nhanh
            end_fragment = 140 + len(html_content)
            end_html = end_fragment + 34  # 34 = len("<!--EndFragment--></body></html>")
            
            formatted_html = html_template.format(
                end_html=end_html,
                end_fragment=end_fragment,
                html_content=html_content
            )
            
            # Copy với retry logic tối ưu
            max_retries = 2  # Giảm số retry để tăng tốc
            for attempt in range(max_retries):
                clipboard_opened = False
                try:
                    win32clipboard.OpenClipboard()
                    clipboard_opened = True
                    win32clipboard.EmptyClipboard()
                    
                    # Plain text nhanh
                    plain_text = (html_content
                        .replace('<br>', '\n')
                        .replace('<br/>', '\n')
                        .replace('<b>', '').replace('</b>', '')
                        .replace('<i>', '').replace('</i>', '')
                        .replace('<u>', '').replace('</u>', '')
                        .replace('<p>', '').replace('</p>', '\n')
                        .replace('&amp;', '&')
                        .replace('&lt;', '<')
                        .replace('&gt;', '>'))
                    
                    win32clipboard.SetClipboardText(plain_text.strip())
                    
                    # HTML format với encoding an toàn
                    html_format = win32clipboard.RegisterClipboardFormat("HTML Format")
                    try:
                        html_bytes = formatted_html.encode('utf-8')
                        win32clipboard.SetClipboardData(html_format, html_bytes)
                    except UnicodeEncodeError:
                        # Fallback: chỉ copy plain text
                        pass
                    
                    win32clipboard.CloseClipboard()
                    clipboard_opened = False
                    return True
                    
                except Exception as inner_e:
                    if clipboard_opened:
                        try:
                            win32clipboard.CloseClipboard()
                        except:
                            pass
                    
                    if attempt == max_retries - 1:
                        raise inner_e
                    else:
                        time.sleep(0.001)  # Micro delay trước retry
                        continue
                
        except Exception as e:
            print(f"Lỗi khi copy văn bản: {e}")
            # Fast fallback
            return ClipboardHandler.copy_text(html_text)
    
    @staticmethod
    def copy_image(image_path: str):
        """Copy ảnh vào clipboard với xử lý tốc độ cao cải tiến"""
        try:
            # Kiểm tra file tồn tại
            if not os.path.exists(image_path):
                print(f"❌ File ảnh không tồn tại: {image_path}")
                return False
            
            print(f"📸 Đang copy ảnh: {image_path}")
            
            # Mở ảnh với Pillow và kiểm tra kích thước
            image = Image.open(image_path)
            width, height = image.size
            print(f"📏 Kích thước ảnh: {width}x{height}")
            
            # Cảnh báo nếu ảnh quá lớn (có thể chậm)
            if width * height > 10000000:  # 10 megapixels
                print(f"⚠️ Ảnh rất lớn ({width}x{height}), có thể mất thời gian...")
            
            # Convert sang RGB nếu cần
            if image.mode != 'RGB':
                image = image.convert('RGB')
                print(f"🔄 Đã convert ảnh từ {image.mode} sang RGB")
            
            # Tạo BMP data
            output = io.BytesIO()
            image.save(output, 'BMP')
            data = output.getvalue()[14:]  # Bỏ qua BMP file header
            output.close()
            
            # Copy vào clipboard với retry logic
            max_retries = 3
            for attempt in range(max_retries):
                clipboard_opened = False
                try:
                    win32clipboard.OpenClipboard()
                    clipboard_opened = True
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardData(win32con.CF_DIB, data)
                    win32clipboard.CloseClipboard()
                    clipboard_opened = False
                    
                    print(f"✅ Đã copy ảnh vào clipboard thành công (attempt {attempt + 1})")
                    
                    # Verification: Kiểm tra xem clipboard có chứa ảnh không - tối ưu tốc độ
                    time.sleep(0.002)  # Giảm từ 5ms xuống 2ms để tăng tốc
                    if ClipboardHandler._verify_image_in_clipboard():
                        return True
                    else:
                        print(f"⚠️ Không thể verify ảnh trong clipboard, thử lại...")
                        if attempt < max_retries - 1:
                            time.sleep(0.005)  # Giảm từ 10ms xuống 5ms delay trước retry
                            continue
                
                except Exception as e:
                    if clipboard_opened:
                        try:
                            win32clipboard.CloseClipboard()
                        except:
                            pass
                    
                    print(f"❌ Lỗi khi copy ảnh (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(0.020)  # 20ms delay trước retry
                        continue
                    else:
                        return False
            
            return False
            
        except Exception as e:
            print(f"❌ Lỗi không mong đợi khi copy ảnh: {e}")
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
            return False
    
    @staticmethod
    def _verify_image_in_clipboard():
        """Kiểm tra xem clipboard có chứa ảnh không"""
        try:
            win32clipboard.OpenClipboard()
            has_image = win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB)
            win32clipboard.CloseClipboard()
            return has_image
        except:
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
            return False
    
    @staticmethod
    def clear_clipboard():
        """Xóa nội dung clipboard"""
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
            return True
        except Exception as e:
            print(f"Lỗi khi xóa clipboard: {e}")
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
            return False

    @staticmethod
    def paste():
        """Thực hiện Ctrl+V"""
        try:
            pyautogui.hotkey('ctrl', 'v')
            return True
        except Exception as e:
            print(f"Lỗi khi paste: {e}")
            return False 