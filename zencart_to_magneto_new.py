#encoding=utf-8
#author:helinyes@gmail.com
import mysql.connector
import sys
import string
import time
import glob
import os
import re
import shutil
config={'host':'127.0.0.1','user':'root','password':'','port':3306 ,'database':'data_to_data','charset':'utf8'}  
config1={'host':'127.0.0.1','user':'root','password':'','port':3306 ,'database':'magento','charset':'utf8'}
zencart_image_dir="F:/images_tmp/"
magento_image_dir="D:/wamp/www/magento/media/catalog/product/"
#所有产品信息，列表类型
products=[]

#连接到zencart数据库
try:  
    cnn=mysql.connector.connect(**config)
    
except mysql.connector.Error as e:  
    print('connect fails!{}'.format(e))


#连接到magento数据库

try:  
    cnn_magento=mysql.connector.connect(**config1)
    
except mysql.connector.Error as e:  
    print('connect fails!{}'.format(e))


#连接到magento数据库

try:  
    cnn_magento1=mysql.connector.connect(**config1)
    
except mysql.connector.Error as e:  
    print('connect fails!{}'.format(e))

#连接到magento数据库

try:  
    cnn_magento2=mysql.connector.connect(**config1)
    
except mysql.connector.Error as e:  
    print('connect fails!{}'.format(e))
	  
#------------------------------------------------#
#------------------------------------------------#
#--------------获取产品信息函数块开始---------------#
#------------------------------------------------#
#------------------------------------------------#
#------------------------------------------------#






#（获取产品描述，返回字典）
def get_productdescription(product_id):
    global cnn
    product_id=str(product_id)
    description={}
    cursor_des=cnn.cursor()
    
    cursor_des.execute("select products_name,products_url from products_description where products_id="+product_id)
    temp_description=cursor_des.fetchone()
    description['name']=temp_description[0]
    description['url']=temp_description[1]
   
    return  description

#（获取产品多图，返回列表）
def get_productaddtionimage(product_image):
    
    base_dir="F:/images_tmp/"
    addtion_image=[]
    image_uri=(base_dir+product_image).replace('.jpg','')
    for i in range(16):
        if os.path.isfile(image_uri+'_'+str(i)+'.jpg'):
            addtion_image.append(product_image.replace('.jpg','')+'_'+str(i)+'.jpg')
           
            
    else:
        #print ("none")
        pass
    return addtion_image

#（获取产品对应目录,返回列表）
def get_product_categories(product_id):
    
    product_id=str(product_id)

    categories=[]
    cursor=cnn.cursor()

    cursor.execute("select categories_id from products_to_categories where products_id="+product_id)
    
    for row in cursor.fetchall():

        for r in row:
            categories.append(r)

    return categories
            
          
#------------------------------------------------#
#------------------------------------------------#
#--------------获取产品信息函数块结束---------------#
#------------------------------------------------#
#------------------------------------------------#
#------------------------------------------------#   
            
#分类id对应字典
categories_to={\
'323':'75','287':'38','288':'38','289':'38','284':'38','315':'70','314':'71','203':'69','204':'76','316':'77',\
'319':'66','318':'73','320':'72','313':'78','317':'79','322':'68','321':'74','304':'59','312':'60','305':'58','306':'62','309':'63','308':'64','301':'65','311':'54',\
'302':'53','300':'56','303':'80','294':'81','231':'48','232':'49','298':'50','234':'82','235':'83','236':'84','237':'45','238':'46',\
'239':'85','240':'51','241':'52','242':'86','245':'40','297':'44','248':'87','293':'43','296':'88','295':'89','252':'42',\
'285':'38','286':'38','292':'41','290':'38','291':'38',\
'279':'90','280':'39','307':'61','310':'91'\
}

#替换特殊字符函数
def cleanchar(str):
    
    str=str.replace('œ','oe')
    str=str.replace('é','e')
    str=str.replace('è','e')
    str=str.replace('ë','e')
    str=str.replace('î','i')
    str=str.replace('ê','e')
    str=str.replace('â','a')
    str=str.replace('à','a')
    str=str.replace('û','u')
    str=str.replace('ü','u')
    str=str.replace('æ','ae')               
    str=str.replace('ô','o')
    str=str.replace('ö','o')
    str=str.replace('ç','c')
    str=str.replace('Î','i')
    str=str.replace('î','i')
    str=str.replace('ï','i')
    str=str.replace("'","")
    str=str.lower()
    
    str=str.strip()
   
    return str


#函数，检查是否有相同的url,有则返回新url
def check_url(product_name,sku):
    cursor1=cnn_magento1.cursor()
    test="Moderne robe de bal Colonne attrayante Seule épaule Longueur ras du sol"
    cursor1.execute("select value from catalog_product_entity_varchar where entity_type_id=10 and attribute_id=96 and value='"+str.strip(product_name)+"'")
    #result=cursor1.execute("select value_id from catalog_product_entity_varchar where entity_type_id=10 and attribute_id=96 and value='"+str.strip(test)+"'")
    #print ("select value_id from catalog_product_entity_varchar where entity_type_id=10 and attribute_id=96 and value='"+str.strip(product_name)+"'")
    row=cursor1.fetchall()
    
    
    if len(row)!=0:
        
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        url=str.strip(re.sub(rstr, "-", product_name))
        url=url.replace('œ','oe')
        url=url.replace('é','e')
        url=url.replace('è','e')
        url=url.replace('ë','e')
        url=url.replace('î','i')
        url=url.replace('ê','e')
        url=url.replace('â','a')
        url=url.replace('à','a')
        url=url.replace('û','u')
        url=url.replace('ü','u')
        url=url.replace('æ','ae')               
        url=url.replace('ô','o')
        url=url.replace('ö','o')
        url=url.replace('ç','c')
        url=url.replace('Î','i')
        url=url.replace('î','i')
        url=url.replace('ï','i')
        url=url.replace("'","")     
        url=url.lower()
        url=url.replace(' ','-')+'_'+sku.lower()
        
        return url
    else:
        
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        url=str.strip(re.sub(rstr, "-", product_name))
        url=url.replace('œ','oe')
        url=url.replace('é','e')
        url=url.replace('è','e')
        url=url.replace('ë','e')
        url=url.replace('î','i')
        url=url.replace('ê','e')
        url=url.replace('â','a')
        url=url.replace('à','a')
        url=url.replace('û','u')
        url=url.replace('ü','u')
        url=url.replace('æ','ae')               
        url=url.replace('ô','o')
        url=url.replace('ö','o')
        url=url.replace('ç','c')
        url=url.replace('Î','i')
        url=url.replace('î','i')
        url=url.replace('ï','i')
        url=url.replace("'","")
        url=url.lower()
        url=url.replace(' ','-')
        
        return url
        


#函数，检查是否有相同的sku,有则跳过
def check_sku(sku):
    
    cursor2=cnn_magento2.cursor()
    test="Moderne robe de bal Colonne attrayante Seule épaule Longueur ras du sol"
    cursor2.execute("select sku from catalog_product_entity where sku="+str.strip(sku))
    #result=cursor1.execute("select value_id from catalog_product_entity_varchar where entity_type_id=10 and attribute_id=96 and value='"+str.strip(test)+"'")
    #print ("select value_id from catalog_product_entity_varchar where entity_type_id=10 and attribute_id=96 and value='"+str.strip(product_name)+"'")
    
    row=cursor2.fetchall()

    
    if len(row)!=0: 
        return True
    else:
        
        return False


 
    
#函数，拷贝zencart产品图片到magento目录并根据产品名重命名
def copy_image_to_magento(image,sku,product_name,if_addition_image=False):
    if if_addition_image:
        #去除路径，获取图片名称
        image_name=os.path.basename(zencart_image_dir+image)
        #获取图片类型（后缀）
        extension = os.path.splitext(image_name)[1]
        #分拆图片名称
        image_all=image_name.split('_')

        #新的图片名称重命名后与产品名称一样（正则替换掉非法字符如/,\，|,*等）
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_image_name_noextension=str.strip(re.sub(rstr, "-", product_name))

        
        new_image_name_noextension=cleanchar(new_image_name_noextension)
        
       
        new_image_name=new_image_name_noextension+"_"+image_all[1]
        
        
        #判断图片是否存在
        if os.path.isfile(magento_image_dir+new_image_name):
            print ("\t\t\t\t存在图片"+new_image_name)
            shutil.copy(zencart_image_dir+image,magento_image_dir+new_image_name_noextension+"_"+sku+"_"+image_all[1])
            return '/'+new_image_name_noextension+"_"+sku+"_"+image_all[1]
        else:
            print ("\t\t\t不存在图片"+new_image_name+"，执行拷贝图片并重命名")
            #不存在图片则拷贝图片到magento目录并重命名
            shutil.copy(zencart_image_dir+image, magento_image_dir+new_image_name)
            return '/'+new_image_name

    else:
        #去除路径，获取图片名称
        image_name=os.path.basename(zencart_image_dir+image)
        #获取图片类型（后缀）
        extension = os.path.splitext(image_name)[1]
        #新的图片名称重命名后与产品名称一样（正则替换掉非法字符如/,\，|,*等）
    
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_image_name_noextension=str.strip(re.sub(rstr, "-", product_name))
        new_image_name_noextension=cleanchar(new_image_name_noextension)

        new_image_name=cleanchar(str.strip(re.sub(rstr, "-", product_name)))+extension
    
    
        #先判断图片是否存在
        if os.path.isfile(magento_image_dir+new_image_name):
            print ("\t\t\t\t存在图片"+magento_image_dir+new_image_name+"\n")
            #存在图片，则加sku
            shutil.copy(zencart_image_dir+image, magento_image_dir+new_image_name_noextension+"_"+sku+extension)
            return '/'+new_image_name_noextension+"_"+sku+extension
           
        else:
            print ("\t\t\t\t不存在图片"+magento_image_dir+new_image_name+"，执行拷贝图片并重命名\n")
            #不存在图片则拷贝图片到magento目录并重命名
            shutil.copy(zencart_image_dir+image, magento_image_dir+new_image_name)
            return '/'+new_image_name
            
	  
##从csv中读取要导入的sku
csv=open('sku.csv')
sku_new=[]
count=0
for line in csv.readlines():
    if(line!='' and count>0):
        line=line.strip('\n')
        sku_new.append("'"+line+"'")
        #print(line)
    count=count+1
#print(sku_new)
skus=','.join(sku_new)
csv.close()
print("总共有"+str(count)+"个产品需要导入")



product_sql='select * from products where products_model in('+skus+')'
print(product_sql)
#print(product_sql)
cursor=cnn.cursor()
cursor1=cnn.cursor()
cursor.execute(product_sql)
cursor.fetchall()

#返回产品总个数
numrows = cursor.rowcount





i=0
cursor1.execute(product_sql)
print ("开始获取zencart数据库产品信息..........")
time.sleep(3)

for row in cursor1.fetchall():
    #临时产品列表
    temp_product=[]
    
    
    #存放产品信息，字典类型
    product_info={}
    #print(row)
    #input()
    for r in row:
        #循环存放产品信息到产品列表
        
        
        temp_product.append(r)
    
    product_info['product_id']=temp_product[0]
    product_info['sku']=temp_product[3]
    product_info['product_image']=temp_product[4]
    product_info['price']=temp_product[5]
    product_info['silhouette']=str(temp_product[6].replace('\n',''))
    product_info['neckline']=temp_product[7].replace('\n','')
    product_info['waist']=temp_product[8].replace('\n','')
    product_info['hemline']=temp_product[9].replace('\n','')
    product_info['sleeve_length']=temp_product[10].replace('\n','')
    product_info['sleeve_type']=temp_product[11].replace('\n','')
    product_info['fabric']=temp_product[12].replace('\n','')
    product_info['embellishment']=temp_product[13].replace('\n','')
    product_info['belt_fabric']=temp_product[14].replace('\n','')
    product_info['back_detail']=temp_product[15].replace('\n','')
    product_info['fully_lined']=temp_product[16].replace('\n','')
    product_info['built_in_bra']=temp_product[17].replace('\n','')
    product_info['body_shape']=temp_product[18].replace('\n','')
    product_info['season']=temp_product[19].replace('\n','')
    product_info['color']=temp_product[20].replace('\n','')
    product_info['special_price']=temp_product[42]
    product_info['master_categories_id']=temp_product[43]
    product_info['product_name']=get_productdescription(product_info['product_id'])['name']
    product_info['addtion_image']=get_productaddtionimage(product_info['product_image'])
    product_info['product_categories']=get_product_categories(product_info['product_id'])

    
    products.append(product_info)
 
    i=i+1
    print("获取到第"+str(i)+"条数据："+product_info['sku'])

cursor1.close
print ("获取数据完毕总共数据为："+str(i)+"条")
time.sleep(1)
print ("开始转存数据到magento库.......")
time.sleep(1)
#----------------------------------------#
#------                              ----#
#------   开始存储数据到magento库      ----#
#------                              ----#
#----------------------------------------#


cursor=cnn_magento.cursor()
cursor.execute("set foreign_key_checks = 0")
not_import_categores_id=[]
p=0
total=int(input("输入想要导入产品的数量:"))
for j in range(len(products)):
    
    product_id=products[j]['product_id']

    product_sku=products[j]['sku']
    product_baseimage=products[j]['product_image']
    product_price=products[j]['price']
    product_silhouette=products[j]['silhouette']
    product_neckline=products[j]['neckline']
    product_waist=products[j]['waist']
    product_hemline=products[j]['hemline']
    product_sleeve_length=products[j]['sleeve_length']
    product_sleeve_type=products[j]['sleeve_type']
    product_fabric=products[j]['fabric']
    product_embellishment=products[j]['embellishment']
    product_belt_fabric=products[j]['belt_fabric']
    product_back_detail=products[j]['back_detail']
    product_fully_lined=products[j]['fully_lined']
    product_built_in_bra=products[j]['built_in_bra']
    product_body_shape=products[j]['body_shape']
    product_season=products[j]['season']
    product_color=products[j]['color']
    product_special_price=products[j]['special_price']
    product_master_categories_id=products[j]['master_categories_id']
    product_name=products[j]['product_name']
    product_addtion_image=products[j]['addtion_image']
    product_to_categories=products[j]['product_categories']

    print(product_sku+':'+str(product_master_categories_id))
    
    #判断两个数据库之间分类是否对应，然后插入数据到magneto库，没有则不执行
    if(check_sku("'"+product_sku+"'")):
        print("存在sku为"+product_sku+"的产品，跳过....")
    else:
        if str(product_master_categories_id) in categories_to.keys():
        
            p=p+1
            if(p>total):
                break
            print ("---第【"+str(p)+"】条："+product_sku)
        
    
            #开始转存数据到catalog_product_entity表
            cursor.execute("insert into catalog_product_entity set entity_type_id=10,attribute_set_id=9,type_id='simple',sku='"+product_sku+"',created_at='2013-05-27 03:18:42',updated_at='2013-05-29 07:59:35',has_options=1,required_options=1")
       

            #获取实体（产品）id
            catalog_entity_id=cursor.lastrowid

            #插入数据到产品分类对应表
            for categories_id in product_to_categories:
            
                if str(categories_id) in categories_to.keys():
                     cursor.execute("insert into catalog_category_product set category_id="+categories_to[str(categories_id)]+",product_id="+str(catalog_entity_id)+",position=1")
                     for i in range(1,4):
                     
                         cursor.execute("insert into catalog_category_product_index set category_id="+str(categories_id)+",product_id="+str(catalog_entity_id)+",position=1,is_parent=1,store_id="+str(i)+",visibility=4")
                     

            #插入产品相关值到实体时间值表
            cursor.execute("insert into catalog_product_entity_datetime set entity_type_id=10,attribute_id=704,store_id=0,entity_id="+str(catalog_entity_id)+",value='2013-05-19 00:00:00'")
            cursor.execute("insert into catalog_product_entity_datetime set entity_type_id=10,attribute_id=705,store_id=0,entity_id="+str(catalog_entity_id)+",value='2013-05-25 00:00:00'")
            cursor.execute("insert into catalog_product_entity_datetime set entity_type_id=10,attribute_id=572,store_id=0,entity_id="+str(catalog_entity_id))
            cursor.execute("insert into catalog_product_entity_datetime set entity_type_id=10,attribute_id=573,store_id=0,entity_id="+str(catalog_entity_id))

            #插入促销价格，如果没促销价格则不执行
            if product_special_price!='':

                cursor.execute("insert into catalog_product_entity_decimal set entity_type_id=10,attribute_id=567,store_id=0,entity_id="+str(catalog_entity_id)+",value="+str(product_special_price))

            #插入产品重量，产品价格
            cursor.execute("insert into catalog_product_entity_decimal set entity_type_id=10,attribute_id=101,store_id=0,entity_id="+str(catalog_entity_id)+",value=2")
            cursor.execute("insert into catalog_product_entity_decimal set entity_type_id=10,attribute_id=99,store_id=0,entity_id="+str(catalog_entity_id)+",value="+str(product_price))
            cursor.execute("insert into catalog_product_entity_decimal set entity_type_id=10,attribute_id=943,store_id=0,entity_id="+str(catalog_entity_id))

            #插入产品相关值到实体整型表(产品状态，关税，前台可见，制造商，enable_googlecheckout)

            cursor.execute("insert into catalog_product_entity_int set entity_type_id=10,attribute_id=273,store_id=0,entity_id="+str(catalog_entity_id)+",value=1")
            cursor.execute("insert into catalog_product_entity_int set entity_type_id=10,attribute_id=274,store_id=0,entity_id="+str(catalog_entity_id)+",value=1")
            cursor.execute("insert into catalog_product_entity_int set entity_type_id=10,attribute_id=526,store_id=0,entity_id="+str(catalog_entity_id)+",value=4")
            cursor.execute("insert into catalog_product_entity_int set entity_type_id=10,attribute_id=102,store_id=0,entity_id="+str(catalog_entity_id))
            cursor.execute("insert into catalog_product_entity_int set entity_type_id=10,attribute_id=903,store_id=0,entity_id="+str(catalog_entity_id)+",value=1")
            cursor.execute("insert into catalog_product_entity_int set entity_type_id=10,attribute_id=935,store_id=0,entity_id="+str(catalog_entity_id)+",value=0")

            #####拷贝产品图片到magento目录并插入到数据库#######

            #拷贝并插入主图
            base_image_in_magento=copy_image_to_magento(product_baseimage,product_sku,product_name,False)
            cursor.execute("insert into catalog_product_entity_media_gallery set attribute_id=703,entity_id="+str(catalog_entity_id)+",value='"+base_image_in_magento+"'")
            gallery_id=cursor.lastrowid
            cursor.execute("insert into catalog_product_entity_media_gallery_value set value_id="+str(gallery_id)+",store_id=0,position=1,disabled=0")
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=493,store_id=0,entity_id="+str(catalog_entity_id)+",value='"+base_image_in_magento+"'")
            #small_image
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=109,store_id=0,entity_id="+str(catalog_entity_id)+",value='"+base_image_in_magento+"'")
            #image
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=106,store_id=0,entity_id="+str(catalog_entity_id)+",value='"+base_image_in_magento+"'")

            #拷贝并插入附加图
            if len(product_addtion_image)!=0:
                iii=2
                for each_image in product_addtion_image:
                    addition_image_in_magento=copy_image_to_magento(each_image,product_sku,product_name,True)
                    cursor.execute("insert into catalog_product_entity_media_gallery set attribute_id=703,entity_id="+str(catalog_entity_id)+",value='"+addition_image_in_magento+"'")
                    addition_id=cursor.lastrowid
                    cursor.execute("insert into catalog_product_entity_media_gallery_value set value_id="+str(addition_id)+",store_id=0,position="+str(iii)+",disabled=0")
                    iii=iii+1
        
            #插入产品相关值到实体文本表(产品描述，段描述等)
            cursor.execute("insert into catalog_product_entity_text set entity_type_id=10,attribute_id=506,store_id=0,entity_id="+str(catalog_entity_id)+",value='short_description&&nbsp&&nbsp'")
            cursor.execute("insert into catalog_product_entity_text set entity_type_id=10,attribute_id=531,store_id=0,entity_id="+str(catalog_entity_id))
            cursor.execute("insert into catalog_product_entity_text set entity_type_id=10,attribute_id=104,store_id=0,entity_id="+str(catalog_entity_id))
            cursor.execute("insert into catalog_product_entity_text set entity_type_id=10,attribute_id=97,store_id=0,entity_id="+str(catalog_entity_id)+",value='description&&nbsp&&nbsp'")


            #插入产品到catalog_product_entity_varchar(产品名称，url等)
            #插入name
            product_name=product_name.replace("'","")
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=96,store_id=0,entity_id="+str(catalog_entity_id)+",value='"+str.strip(product_name)+"'")
            #插入url_key
            url=check_url(product_name,product_sku)
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=481,store_id=0,entity_id="+str(catalog_entity_id)+",value='"+str.strip(url)+"'")
            #manufacture
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=940,store_id=0,entity_id="+str(catalog_entity_id))
            #msrp_enabled
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=941,store_id=0,entity_id="+str(catalog_entity_id)+",value=2")
            #msrp_display_actual_price_type
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=942,store_id=0,entity_id="+str(catalog_entity_id)+",value=4")
            #meta_title
            #cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=103,store_id=0,entity_id="+str(catalog_entity_id)+",value=4")
            #meta_description
            #cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=105,store_id=0,entity_id="+str(catalog_entity_id)+",value=4")

            #thumbnail
            #print ("insert into `catalog_product_entity_varchar` set `entity_type_id`=10,`attribute_id`=493,`store_id`=0,`entity_id`="+str(catalog_entity_id)+",`value`='no_selection'")
            #input()
            #cursor.execute("insert into `catalog_product_entity_varchar` set `entity_type_id`=10,`attribute_id`=493,`store_id`=0,`entity_id`="+str(catalog_entity_id)+",`value`='no_selection'")
        
            #custom_design
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=571,store_id=0,entity_id="+str(catalog_entity_id))
            #options_container
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=836,store_id=0,entity_id="+str(catalog_entity_id)+",value='container2'")
            #page_layout
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=931,store_id=0,entity_id="+str(catalog_entity_id))
            #gift_message_available
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=562,store_id=0,entity_id="+str(catalog_entity_id)+",value=1")

            #thumbnail_label
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=881,store_id=0,entity_id="+str(catalog_entity_id))
            #small_image_label
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=880,store_id=0,entity_id="+str(catalog_entity_id))

            #image_label
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=879,store_id=0,entity_id="+str(catalog_entity_id))
        
            #url_path
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=570,store_id=0,entity_id="+str(catalog_entity_id)+",value='"+str.strip(url)+"'")
            cursor.execute("insert into catalog_product_entity_varchar set entity_type_id=10,attribute_id=570,store_id=1,entity_id="+str(catalog_entity_id)+",value='"+str.strip(url)+"'")

            #插入catalog_product_flat(1,2,3)表
            for aa in range(1,4):
                cursor.execute("insert into catalog_product_flat_"+str(aa)+" set entity_id="+str(catalog_entity_id)+",attribute_set_id=9,type_id='simple',created_at='2013-05-31 06:43:21'\
            ,description='test test ，&&nbsp',enable_googlecheckout=1,has_options=1,image='"+base_image_in_magento+"',is_recurring=0,msrp_display_actual_price_type=4\
            ,msrp_enabled=2,name='"+product_name+"',price="+str(product_price)+",required_options=1,short_description='short description &&nbsp',sku='"+product_sku+"'\
            ,small_image='"+base_image_in_magento+"',special_from_date='2013-05-19 00:00:00',special_price="+str(product_special_price)+",special_to_date='2014-06-27 00:00:00'\
            ,tax_class_id=1,thumbnail='no_selection',updated_at='2013-05-31 10:38:25',url_key='"+url+"',url_path='"+url+"',visibility=4,weight=2")
            for aa in range(1,4):
                cursor.execute("insert into catalog_product_index_eav set entity_id="+str(catalog_entity_id)+",attribute_id=903,store_id="+str(aa)+",value=1")
                cursor.execute("insert into catalog_product_index_eav set entity_id="+str(catalog_entity_id)+",attribute_id=971,store_id="+str(aa)+",value=128")

            #catalog_product_index_eav_idx
            for aa in range(1,4):
                cursor.execute("insert into catalog_product_index_eav_idx set entity_id="+str(catalog_entity_id)+",attribute_id=903,store_id="+str(aa)+",value=1")

            #catalog_product_index_price
            for aa in range(5):
                cursor.execute("insert into catalog_product_index_price set entity_id="+str(catalog_entity_id)+",customer_group_id="+str(aa)+",website_id=1,tax_class_id=1,price="+str(product_price)+"\
            ,final_price="+str(product_special_price)+",min_price="+str(product_special_price)+",max_price="+str(product_special_price))
            #catalog_product_index_price_idx
            for aa in range(5):
                cursor.execute("insert into catalog_product_index_price_idx set entity_id="+str(catalog_entity_id)+",customer_group_id="+str(aa)+",website_id=1,tax_class_id=1,price="+str(product_price)+"\
            ,final_price="+str(product_special_price)+",min_price="+str(product_special_price)+",max_price="+str(product_special_price))    
            #catalog_product_website
            cursor.execute("insert into catalog_product_website set product_id="+str(catalog_entity_id)+",website_id=1")

            #cataloginventory_stock_item
            cursor.execute("insert into cataloginventory_stock_item set product_id="+str(catalog_entity_id)+",stock_id=1,qty=1000,min_qty=0,use_config_min_qty=1,is_qty_decimal=0,\
        backorders=0,use_config_backorders=1,min_sale_qty=1,use_config_min_sale_qty=1,max_sale_qty=0,use_config_max_sale_qty=1,is_in_stock=1,use_config_notify_stock_qty=1,\
        manage_stock=0,use_config_manage_stock=1,stock_status_changed_auto=0,use_config_qty_increments=1,qty_increments=0,use_config_enable_qty_inc=1,enable_qty_increments=0,\
        is_decimal_divided=0")
            #cataloginventory_stock_status
            cursor.execute("insert into cataloginventory_stock_status set product_id="+str(catalog_entity_id)+",website_id=1,stock_id=1,qty=1000,stock_status=1")

            #cataloginventory_stock_status_idx
       
            cursor.execute("insert into cataloginventory_stock_status_idx set product_id="+str(catalog_entity_id)+",website_id=1,stock_id=1,qty=1000,stock_status=1")

            cnn_magento.commit()
        
        
        





        
        else:
            print ("\t\t\tid["+str(product_master_categories_id)+"]在magneto库中没有与之对应的id，跳过此分类")
            not_import_categores_id.append(str(product_master_categories_id))
            

cursor.execute("set foreign_key_checks = 1")
cursor.close
print ("一共有"+str(len(not_import_categores_id))+"没导入")
    
    
    
    
    
    
    

    
	  


	  
