man_pages_out = []
man_pages_in = [
    'java-config-2.1',
]

foreach man_page : man_pages_in
    man_pages_out += configure_file(
        input : man_page,
        output : man_page,
        configuration : conf_data
    )
endforeach

install_man(man_pages_out)
