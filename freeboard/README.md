Configuring dweet.io and viewing freeboard UI to be imported by each table.

Crating Dweet instances:
- If you have are at table-1 then your dweet instance name in your app should be cisco-table-1.
    Snippet from package_config.ini for reference:
        [dweet]
        # Set to no to disable it
        enabled: yes
        server: dweet.io
        name: cisco-table-1
- Once your done with above step, start your app and check this url : https://dweet.io/follow/<your dweet instance name>,
        and you should be able see the data posted by your app.
- Now you have successfully created dweet instance and pushing the data to it.

# Once your app successfully pushing the data to the above created dweet.io instance,
    check the bwlow URL's for the freeboard UI.
    * cisco-table-1 - https://freeboard.io/board/0MxLOD
    * cisco-table-2 - https://freeboard.io/board/FJJLOD
    * cisco-table-3 - https://freeboard.io/board/a86MOD
    * cisco-table-4 - https://freeboard.io/board/rreMOD
    * cisco-table-5 - https://freeboard.io/board/Q2kMOD
    * cisco-table-6 - https://freeboard.io/board/dQYMOD
    * cisco-table-7 - https://freeboard.io/board/62jNOD
    * cisco-table-8 - https://freeboard.io/board/TpoNOD
    * cisco-table-9 - https://freeboard.io/board/08oOOD

