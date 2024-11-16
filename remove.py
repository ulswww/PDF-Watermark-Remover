from pypdf import PdfReader, PdfWriter, generic

def removeWatermark(input_fname: str, output_fname: str):

    with open(input_fname, "rb") as input_file:

        reader = PdfReader(input_file)
        writer = PdfWriter()

        for n in range(len(reader.pages)):

            page = reader.pages[n]
            del page["/Contents"][-1]
            del page["/Annots"][-1]

            writer.add_page(page)

        outlines = reader.outline

        def process_outline_item(item, parent=None):
                new_outline = None
                if isinstance(item, generic.Destination):
                    # 如果是简单的目标，直接创建对应的书签并添加到目标PDF的大纲中
                    page_number = reader.get_destination_page_number(item)
                    new_outline = writer.add_outline_item(
                        item.title, page_number, parent=parent
                    )
                elif isinstance(item, generic.List):
                    # 如果是包含子项的大纲项，先创建对应书签，再递归处理子项
                    pre_outline = None
                    for k in item:
                        is_child = isinstance(k, generic.List)
                        tmp_outline = process_outline_item(k, parent= pre_outline if is_child else parent)
                        if tmp_outline :
                            pre_outline = tmp_outline

                return new_outline

    parent = None

    for top_level in outlines:
       parent = process_outline_item(top_level, parent= parent)


    with open(output_fname, "wb") as output_file:

        writer.write(output_file)

if __name__ == "__main__":

    import sys
    if len(sys.argv) == 1:
        removeWatermark("Al-Brooks-Trading-Price-Action-Ranges_目录版.pdf", "Al-Brooks-Trading-Price-Action-Ranges_目录版_no_water.pdf")
    elif len(sys.argv) == 2:
        removeWatermark(sys.argv[1], sys.argv[1][0:-4]+"_no_water.pdf")
    elif len(sys.argv) == 3:
        removeWatermark(sys.argv[1], sys.argv[2])
    else:
        removeWatermark("input.pdf","out.pdf")
