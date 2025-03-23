import aiohttp,requests,asyncio, aiofiles
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from aiohttp import ClientTimeout
import os

creator = "CREATOR_NAME" (Taylor lavie)
service = "SERVICE_NAME" (onlyfans,fansly)
basepath = "DIRECTORY_WHERE_YOU_WANT TO SAVE" + '\\'
path_to_save = basepath + "\\" f"{creator}" + '.txt'
async def get_lbe(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            html = await res.json()
            return html
        
async def append_links(link):
    async with aiofiles.open(path_to_save,'a') as f:
        await f.write(link +'\n')

"""
This Main() Needs Some Repair

"""
# async def main():

#     urls = [f"https://coomer.su/api/v1/{service}/user/{creator}?o={i}" for i in range(50,501) if i%50 ==0]
#     tasks = [get_lbe(url) for url in urls]
#     responses = await asyncio.gather(*tasks)
#     for response in responses:
#         file_path = response.get('file', {}).get('path', None)
#         if file_path:
#             # Append the file path to the text file
#             await append_links(str(file_path))
#     datalinks = []
#     text = await get_lbe("https://coomer.su/api/v1/{service}/user/{creator}?o=50")
#     for url in urls:
#         text = await get_lbe(url)
#         datalinks.append(text)
#     links = await asyncio.gather(*datalinks)
#     for link in links:
#         file_path = link.get('file', {}).get('path',None)
#         await append_links(str(file_path))
#     for data in text:
#         file_path = data.get('file', {}).get('path', None)
#         print(file_path)
#         if not os.path.exists(f'{path_to_save}'):
#             with open(f"{path_to_save}", 'w') as f:
#                 if file_path != None:
#                     f.write(f"{file_path}\n")
#         else:
#             with open(f"{path_to_save}", 'a') as f:
#                 if file_path != None:
#                     f.write(f"{file_path}\n")

async def main():
    # URLs to fetch
    urls = [f"https://coomer.su/api/v1/{service}/user/{creator}?o={i}" for i in range(50, 1201, 50)]
    urls.insert(0,f"https://coomer.su/api/v1/{service}/user/{creator}")
    
    # List of tasks to fetch the data
    tasks = [get_lbe(url) for url in urls]

    # wait till all the tasks are gathers as response
    responses = await asyncio.gather(*tasks)

    # Loop through each response
    for response in responses:
        # print(f"Response content: {response}")  # To ConsoleLog the response

        # If the response is a list, iterate through it (for example, extracting file paths)
        # if isinstance(response, list):
            # Iterate through the list and extract file paths
        for item in response:
            if isinstance(item, dict):
                file_path = item.get('file', {})
                path = file_path.get('path', None)
                name = file_path.get('name', None)
                if path and name:
                    formatted_link = f"{path}?f={name}"
                    await append_links(str(formatted_link))
        # else:
        #     # Get the path from json/Dict
        #     print("else is working")
        #     file_path = response.get('file', {}).get('name', None)
        #     if file_path:
        #         await append_links(str(file_path))






"""
RUN TO GET URLS AND APPEND THEM
"""

# if __name__ == "__main__":
        # print(url)
asyncio.run(main())



"""
----------Downloading Part Here---------------

"""

"""
Change the Semaphore Digit to download more fast. But it will Give error (SSL error). So do it at your own risk

"""
semaphore = asyncio.Semaphore(2)
async def dimg(url,filename):
    async with semaphore:
        try:
            async with aiohttp.ClientSession() as session:
                timeout = ClientTimeout(total=60)
                async with session.get(url,timeout=timeout) as resp:
                    resp.raise_for_status()
                    with open(filename, 'wb') as f:
                        f.write(await resp.read())
        except Exception as e:
            print(f"Error: {e}")

async def download_images(basedataimg):
    tasks=[]
    for i,url in enumerate(basedataimg):
        filename = f"{basepath}img{i+1}.jpg"
        tasks.append(dimg(url.strip(),filename))
    await asyncio.gather(*tasks)

async def download_videos(basedatavid):
    tasks=[]
    for i,url in enumerate(basedatavid):
        filename = f"{basepath}vid{i+1}.mp4"
        tasks.append(dimg(url.strip(),filename))
    await asyncio.gather(*tasks)

"""
Run any one of these to download image/video

"""

def start_video_download():
    with open(f"{path_to_save}",'r') as f:
        datatext = f.readlines()
    basedatavid = []
    for dt in datatext:
        if dt.strip().endswith(".mp4"):
            basedatavid.append(f"https://n4.coomer.su/data{dt}")   
    asyncio.run(download_videos(basedatavid))

def start_image_download():
    with open(f"{path_to_save}",'r') as f:
        datatext = f.readlines()
    basedataimg = []
    for dt in datatext:
        if dt.strip().endswith(".jpg"):
            # basedataimg.append(f"https://img.coomer.su/thumbnail/data{dt}")
            basedataimg.append(f"https://n4.coomer.su/data{dt}")
    asyncio.run(download_images(basedataimg))

start_image_download()
# start_video_download()
"""
------------Downloading Part END---------------

"""
