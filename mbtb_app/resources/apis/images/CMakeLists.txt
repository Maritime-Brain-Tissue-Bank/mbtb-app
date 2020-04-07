cmake_minimum_required(VERSION 3.7)
project(CZIImages)
set(CMAKE_CXX_STANDARD 11)



# Configure required libraries
if(UNIX) # Darwin or Linux

    find_package(Boost REQUIRED COMPONENTS system thread log program_options chrono)
    find_package(Threads REQUIRED)

    if(APPLE)
        set( OPENSSL_ROOT_DIR "/usr/local/opt/openssl/")
        find_package(OpenSSL REQUIRED)
        if ( OPENSSL_FOUND )
            message(STATUS "OpenSSL Found: ${OPENSSL_VERSION}")
            message(STATUS "OpenSSL Include: ${OPENSSL_INCLUDE_DIR}")
            message(STATUS "OpenSSL Libraries: ${OPENSSL_LIBRARIES}")
        endif()

        find_package(cpprestsdk REQUIRED)
    endif()

else()
    message(FATAL_ERROR "-- Platform not supported :( ")
endif()



# Configure compiler
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")

    message("-- configuring clang options")
    set(CMAKE_CXX_FLAGS "-arch x86_64 -std=c++11 -stdlib=libc++ -DBOOST_LOG_DYN_LINK -Wno-deprecated-declarations")

elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")

    message("-- configuring gcc options")

    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=gnu++11 -DBOOST_LOG_DYN_LINK")

endif()



# source files
add_executable(${PROJECT_NAME}  ./src/CZIImage.cpp ./src/czi_image/CZIController.cpp
                                ./src/rest_base/Controller.cpp ./src/db/DBConnection.cpp
        )



# include header files
set(REST_INCLUDE_DIR "./src/rest_base/include/")  # REST Base dir
set(CZI_IMAGE_INCLUDE_DIR "./src/czi_image/")  # CZI Image dir
set(DB_INCLUDE_DIR "./src/db/include/")  # DB dir
set(MYSQLCONN_INCLUDE_DIR "/usr/local/Cellar/mysql-connector-c++/8.0.19/include/")  # mysqlx connector
set(HEADER_SEARCH_PATHS ${Boost_INCLUDE_DIR} ${OPENSSL_INCLUDE_DIR}
                        ${REST_INCLUDE_DIR} ${CZI_IMAGE_INCLUDE_DIR}
                        ${MYSQLCONN_INCLUDE_DIR} ${DB_INCLUDE_DIR}
        )

# display msg: header file path
message(CZI_IMAGE " ${CZI_IMAGE_INCLUDE_DIR}")
message(REST " ${REST_INCLUDE_DIR}")
message(MYSQLCONN " ${MYSQLCONN_INCLUDE_DIR}")



# library search
if(APPLE)
    set(ZIP_LIBRARY "/usr/local/Cellar/zlib/1.2.11/lib/libz.dylib")
    set(MYSQLCONN_LIBS "/usr/local/Cellar/mysql-connector-c++/8.0.19/lib/libmysqlcppconn8.2.dylib")
    set(LIBRARIES_SEARCH_PATHS ${OPENSSL_LIBRARIES} ${Boost_LIBRARIES} ${ZIP_LIBRARY} ${MYSQLCONN_LIBS})
endif()

# display msg: libraries path
message(BOOST_LIBS " ${Boost_LIBRARIES}")
message(MYSQLCONN_LIBS " ${MYSQLCONN_LIBS}")
message(LIBRARIES_SEARCH_PATHS " ${LIBRARIES_SEARCH_PATHS}")


include_directories(${HEADER_SEARCH_PATHS})

if (APPLE)
    target_link_libraries(${PROJECT_NAME} cpprestsdk::cpprest)
    target_link_libraries(${PROJECT_NAME} "-framework CoreFoundation")
    target_link_libraries(${PROJECT_NAME} "-framework Security")
    target_link_libraries(${PROJECT_NAME} ${LIBRARIES_SEARCH_PATHS})
    set_target_properties(${PROJECT_NAME} PROPERTIES LINK_FLAGS "-W1, -F/Library/Frameworks")
endif ()
