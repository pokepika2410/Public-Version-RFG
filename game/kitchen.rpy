label game_start():
    if fridge.all_checked():
        jump game_end
    window hide
    hide screen focus_dialogue
    hide screen focus_menu
    $ renpy.pause(hard=True)

label food_navi(food):
    show screen focus_dialogue
    if not food.checked:
        call expression "view_{}".format(food.key)
        show screen focus_menu
        menu: 
            "Check":
                hide screen focus_menu
                $ fridge.update(food.check())
                call check_nav(food)
            "Leave it":
                hide screen focus_menu
                "I'll check on this later."
    else:
        call check_nav(food)
    jump game_start

label check_nav(food):
    call expression "check_{}".format(food.key)
    if food.key not in ["broccoli", "butter", "ketchup"]:
        show screen focus_menu
        if food.key == "tomatoes":
            if f_tomatoes.xstart == 393:
                return
            menu: 
                "Fruit":
                    hide screen focus_menu
                    call expression "fruit_{}".format(food.key)
                "Vegetable":
                    hide screen focus_menu
                    call expression "veg_{}".format(food.key)
        elif food.key == "cake":
            menu: 
                "Keep":
                    hide screen focus_menu
                    call expression "keep_{}".format(food.key)
                "Put in Freezer":
                    hide screen focus_menu
                    $ fridge.toss(food)
                    call expression "freezer_{}".format(food.key)
        else:
            menu:
                "Keep":
                    hide screen focus_menu
                    call expression "keep_{}".format(food.key)
                "Toss":
                    hide screen focus_menu
                    $ fridge.toss(food)
                    call expression "toss_{}".format(food.key)
    return

# Transforms ------------------------------------------------------------------
transform focus_effect:
    on idle:
        linear 0.15 zoom 1
    on hover:
        ease 0.15 zoom 1.2

#--------------------------------------------------------------------------
# KITCHEN SCREEN
#--------------------------------------------------------------------------
screen kitchen(fridge):
    zorder 0

    # thermo
    imagebutton:
        idle "/images/food/thermo.png"
        xpos 460
        ypos 224
        xanchor 0.5 yanchor 0.5
        focus_mask True
        action Jump("check_thermo")
        at focus_effect

    # populate fridge
    for i in fridge.items:
        imagebutton:
            idle "/images/food/{}.png".format(i.key)
            xpos i.xstart
            ypos i.ystart
            xanchor 0.5 yanchor 0.5
            focus_mask True
            action Call("food_navi", i)
            at focus_effect

screen focus_dialogue:
    zorder 0
    modal True
    imagebutton:
        idle Solid("#0000")
        action renpy.curry(renpy.end_interaction)(True)
    key "K_SPACE" action renpy.curry(renpy.end_interaction)(True)
    # key "mouseup_4" action ShowMenu('history') # access log on scrollup

screen focus_menu:
    zorder 0
    modal True
    image Solid("#0000")