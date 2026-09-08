package main

import "fmt"

// black red tree rule:
// root 為黑
// 不能有兩個連續紅色
//

type Color bool

const (
	Red   Color = false
	Black Color = true
)

type Node struct {
	Value  int
	Color  Color
	Left   *Node
	Right  *Node
	Parent *Node
}

type RBTree struct {
	Root *Node
	Nil  *Node
}

func NewRBTree() *RBTree {
	nilNode := &Node{Color: Black}
	return &RBTree{Root: nilNode, Nil: nilNode}
}

func LeftRotate(tree *RBTree, x *Node) {
	y := x.Right

	x.Right = y.Left
	if x.Right != tree.Nil {
		x.Right.Parent = x
	}

	y.Parent = x.Parent
	if x.Parent == tree.Nil {
		tree.Root = y
	} else if x == x.Parent.Left {
		x.Parent.Left = y
	} else {
		x.Parent.Right = y
	}

	y.Left = x
	x.Parent = y
}

func RightRotate(tree *RBTree, x *Node) {
	y := x.Left

	x.Left = y.Right
	if x.Left != tree.Nil {
		x.Left.Parent = x
	}

	y.Parent = x.Parent
	if x.Parent == tree.Nil {
		tree.Root = y
	} else if x == x.Parent.Left {
		x.Parent.Left = y
	} else {
		x.Parent.Right = y
	}

	y.Right = x
	x.Parent = y
}

func (tree *RBTree) Insert(value int) {
	node := &Node{
		Value: value,
		Color: Red,
		Left:  tree.Nil,
		Right: tree.Nil,
	}
	if tree.Root == tree.Nil {
		node.Color = Black
		node.Parent = tree.Nil
		tree.Root = node
		return
	}

	current := tree.Root
	parent := tree.Nil
	for current != tree.Nil {
		parent = current
		if value <= parent.Value {
			current = current.Left
		} else {
			current = current.Right
		}
	}

	node.Parent = parent
	if value <= parent.Value {
		parent.Left = node
	} else {
		parent.Right = node
	}

	tree.Fixup(node)
}

func (tree *RBTree) Fixup(node *Node) {
	if node.Parent.Color == Black {
		tree.Root.Color = Black
		return
	}

	//find the uncle
	parent := node.Parent
	grandParent := parent.Parent
	parentIsLeft := parent == grandParent.Left

	var uncle *Node
	if parent == parent.Parent.Left {
		uncle = parent.Parent.Right
	} else {
		uncle = parent.Parent.Left
	}

	if uncle.Color == Red {
		parent.Color = Black
		uncle.Color = Black
		grandParent.Color = Red
		tree.Fixup(grandParent)
		return
	}

	// case 2: uncle is black and node at "內側"
	if parentIsLeft && node == parent.Right {
		LeftRotate(tree, parent)
		node = parent
		parent = node.Parent
	} else if !parentIsLeft && node == parent.Left {
		RightRotate(tree, parent)
		node = parent
		parent = node.Parent
	}

	// case 3: uncle is black and node at "外側"
	parent.Color = Black
	grandParent.Color = Red
	if parentIsLeft {
		RightRotate(tree, grandParent)
	} else {
		LeftRotate(tree, grandParent)
	}
}

func (tree *RBTree) Print() {
	tree.printNode(tree.Root, "", true)
}

func (tree *RBTree) printNode(node *Node, prefix string, isLeft bool) {
	if node == tree.Nil {
		return
	}

	color := "R"
	if node.Color == Black {
		color = "B"
	}

	fmt.Printf("%s%s── %d(%s)\n", prefix, map[bool]string{true: "L", false: "R"}[isLeft], node.Value, color)

	newPrefix := prefix
	if isLeft {
		newPrefix += "│   "
	} else {
		newPrefix += "    "
	}

	tree.printNode(node.Left, newPrefix, true)
	tree.printNode(node.Right, newPrefix, false)
}

func main() {
	tree := NewRBTree()

	values := []int{10, 20, 30, 15, 25, 5, 1}
	for _, v := range values {
		tree.Insert(v)
		fmt.Printf("Insert %d:\n", v)
		tree.Print()
		fmt.Println()
	}
}
