/*
 * Copyright 2004-2008 Sun Microsystems, Inc. All Rights Reserved.
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER
 * 
 * This code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2
 * only, as published by the Free Software Foundation.
 * 
 * This code is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License version 2 for more details (a copy is
 * included in the LICENSE file that accompanied this code).
 * 
 * You should have received a copy of the GNU General Public License
 * version 2 along with this work; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 * 02110-1301 USA
 * 
 * Please contact Sun Microsystems, Inc., 16 Network Circle, Menlo
 * Park, CA 94025 or visit www.sun.com if you need additional
 * information or have any questions.
 */
package com.sun.cldc.jna;



////import java.lang.annotation.ElementType;
////import java.lang.annotation.Retention;
////import java.lang.annotation.RetentionPolicy;
////import java.lang.annotation.Target;


/**
 * <b>NOT YET IMPLEMENTED</b>
 *
 * The Includes annotation can be applied to the top-level interface declarations in a JNA
 * Library declaration to indicate the C include files that contain the relevent #defines and structure definitions
 * for that library
 * 
 * Example:
 * 
 *    &#64;Includes( "<errno.h>",
 *               "<fcntl.h>",
 *                "<sys/stat.h>")
 *    public interface LibC extends LibraryImport { ... }
 * 
 */


////@Retention(RetentionPolicy.RUNTIME)
////@Target(ElementType.TYPE)


public


////        @

        interface
        Includes {

    String[] value();
}
